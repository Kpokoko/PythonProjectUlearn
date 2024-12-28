import csv
from django.core.management import BaseCommand
from django.db.models import F, Avg
from django.db.models.functions import Substr, Round
import os
from analytics.models import Vacancy
import pandas as pd


def get_exchange_rates(date, salary_currency):
    '''
    Достаёт по api информацию с сервера
    :param date: интересующая нас дата
    :param salary_currency: кодовое имя валюты
    :return: курс валюты на запрошенную дату
    '''
    date_str = date.strftime('%d/%m/%Y')
    url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date_str}"  # Формируем URL для запроса с указанной датой
    data = pd.read_xml(url, encoding="windows-1251")  # Загружаем и парсим XML данные с сайта ЦБ
    currency = float(data[data['CharCode'] == salary_currency]['Value'].values[0].replace(',', '.')) if not data[
        data['CharCode'] == salary_currency].empty else 0
    return currency  # Возвращаем курс


class Command(BaseCommand):
    help = 'Calculate and save salary statistics by year to a CSV file'

    def handle(self, *args, **options):
        data = Vacancy.objects.all()
        for item in data:
            if item.salary_currency != 'RUR':
                date = item.published_at.replace(day=1)
                exchange_rate = get_exchange_rates(date, item.salary_currency)
                item.salary_from = float(item.salary_from or 0) * exchange_rate
                item.salary_to = float(item.salary_to or 0) * exchange_rate
            else:
                item.salary_from = float(item.salary_from or 0)
                item.salary_to = float(item.salary_to or 0)

            item.salary_from = 0 if item.salary_from is None else item.salary_from
            item.salary_to = 0 if item.salary_to is None else item.salary_to

        data = (data.annotate(year=Substr('published_at', 1, 4))
                .values('year')
                .annotate(avg_salary=Round(Avg((F('salary_from') + F('salary_to')) / 2), 2)))

        # Определяем путь для сохранения файла
        file_path = os.path.join(os.getcwd(), "salary_by_year.csv")

        # Сохраняем данные в CSV-файл
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Year', 'Avg Salary'])
            for row in data:
                writer.writerow([row['year'], row['avg_salary'] or 0])

        self.stdout.write(self.style.SUCCESS('Successfully generated general_statistics.csv'))
