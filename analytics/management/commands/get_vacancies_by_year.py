from django.core.management import BaseCommand
from django.db.models import Count
from django.db.models.functions import Substr
from analytics.models import Vacancy, Vacancies_by_year


class Command(BaseCommand):
    def handle(self, *args, **options):
        Vacancies_by_year.objects.all().delete()
        data = Vacancy.objects.filter(published_at__isnull=False)

        data = (data.annotate(year=Substr('published_at', 1, 4))  # Аннотируем данные, извлекая год из даты публикации
                .values('year')  # Группируем данные по годам
                .annotate(number_of_vacancies=Count('published_at')))  # Считаем количество вакансий по годам

        # Сохраняем новые данные в модель Vacancies_by_year
        for item in data:
            Vacancies_by_year.objects.create(vacancy_count=item['number_of_vacancies'], year=item['year'])
