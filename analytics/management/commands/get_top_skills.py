from django.core.management.base import BaseCommand
from django.db.models import Count
from django.db.models.functions import ExtractYear
from collections import defaultdict, Counter
from analytics.models import Vacancy, Top_skills


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Удалим старые данные
        Top_skills.objects.all().delete()

        # Получаем данные вакансий с ненулевым полем published_at
        data = Vacancy.objects.filter(published_at__isnull=False)

        # Аннотируем и группируем по годам
        data = (data.annotate(year=ExtractYear('published_at'))
                .values('year', 'key_skills')
                .annotate(number_of_vacancies=Count('id')))

        skills_by_year = defaultdict(Counter)

        for item in data:
            year = item['year']
            skills_str = item['key_skills']

            # Разбиваем строку навыков на отдельные навыки, разделенные запятыми и переносами строк
            if isinstance(skills_str, str):
                skills_list = []
                for separator in [',', '\n']:
                    skills_list.extend(skill.strip() for skill in skills_str.split(separator) if skill.strip())

                for skill in skills_list:
                    skills_by_year[year][skill] += 1

        # Оставляем топ-20 навыков для каждого года и сортируем
        top_skills_by_year = {year: dict(counts.most_common(20)) for year, counts in skills_by_year.items()}
        sorted_top_skills = sorted(top_skills_by_year.items())

        # Сохраняем в модель Top_skills
        for year, skills_freq in sorted_top_skills:
            Top_skills.objects.create(year=year, skills_list=skills_freq)
