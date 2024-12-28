from django.core.management.base import BaseCommand
from django.db.models import F, Avg, Count
from django.db.models.functions import Round
from analytics.models import Vacancy, Currency, Salary_by_city

class Command(BaseCommand):
    help = 'Generate general statistics of vacancies'

    def handle(self, *args, **kwargs):
        Salary_by_city.objects.all().delete()
        data = Vacancy.objects.all()
        bd = Currency.objects.all()

        # Преобразуем bd в словарь для более удобного доступа
        currency_dict = {(item.date.strftime('%Y-%m-%d'), item.currency_code): item.currency for item in bd}

        # Преобразуем зарплаты в рубли
        for item in data:
            if item.salary_currency and item.salary_currency != 'RUR':
                date = item.published_at.replace(day=1)
                exchange_rate = currency_dict.get((date.strftime('%Y-%m-%d'), item.salary_currency), 0)
                item.salary_from = float(item.salary_from or 0) * exchange_rate
                item.salary_to = float(item.salary_to or 0) * exchange_rate

        # Фильтруем вакансии, чтобы исключить те, у которых зарплата выше 10 миллионов рублей
        data = data.filter(salary_from__lte=10000000, salary_to__lte=10000000)

        # Рассчитываем среднее значение (salary_from + salary_to) / 2
        data = data.annotate(avg_salary=((F('salary_from') + F('salary_to')) / 2))
        total = data.count()

        data = data.annotate(area=F('area_name'))  # Аннотируем названия городов
        data = data.values('area')  # Группируем данные по названиям городов
        data = data.annotate(count_vacancies=Count('area'))  # Считаем количество вакансий
        data = data.filter(count_vacancies__gt=total * 0.01)  # Фильтруем города с количеством вакансий более 1%
        data = data.annotate(avg_salary=Round(Avg('avg_salary'), 2))  # Рассчитываем среднюю зарплату

        data = data.order_by('-avg_salary')  # Рассчитываем среднюю зарплату по годам и округляем до 2 знаков после запятой

        # Сохраняем новые данные в модель Salary_by_year
        for item in data:
            Salary_by_city.objects.create(area_name=item['area'], avg_salary=item['avg_salary'])

