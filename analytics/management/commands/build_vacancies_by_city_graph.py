from django.core.management.base import BaseCommand
import matplotlib.pyplot as plt
import numpy as np
from analytics.models import Vacancies_by_city
import pandas as pd


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = Vacancies_by_city.objects.all().values('area_name', 'vacancy_count', 'vacancy_share')
        stats = self.get_salary_stats(data)
        name = 'Доля вакансий по городам'

        fig, ax = plt.subplots()
        self.generate_pie_diagram(stats, ax, name)

        fig.tight_layout()  # Оптимизация расположения графиков
        plt.savefig('analytics\\static\\analytics\\img\\graphs\\vacancies_by_city.png')  # Сохранение графика в PNG файл
        plt.show()  # Отображение графиков

    def get_salary_stats(self, data):
        """
        Преобразование QuerySet в словарь для построения графика
        :param data: QuerySet с данными о вакансиях
        :return: распределение вакансий по городам
        """
        df = pd.DataFrame(data)
        vacancies_by_city = df.set_index('area_name')['vacancy_share'].to_dict()
        other_share = sum(vacancies_by_city.values())
        vacancies_by_city['Остальные'] = 1 - other_share
        return vacancies_by_city  # Возврат распределения вакансий по городам

    def generate_pie_diagram(self, stats, ax, name):
        """
        Генерирует круговую диаграмму
        :param stats: обработанные входные данные
        :param ax: полотно для рисования диаграммы
        :param name: название диаграммы
        """
        ax.pie(
            list(stats.values()),
            labels=list(stats.keys()),
            textprops={'fontsize': 6},
        )
        ax.set_title(name, fontsize=8)  # Установка заголовка диаграммы
