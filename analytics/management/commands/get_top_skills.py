from django.core.management.base import BaseCommand
from analytics.models import Vacancy, Top_skills


class Command(BaseCommand):
    def handle(self, *args, **options):
        Top_skills.objects.all().delete()
        data = Vacancy.objects.all()
        skills_by_year = {}
        for item in data:
            year = item.published_at.year
            skills_str = item.key_skills

            # Разбиваем строку навыков на отдельные навыки, разделенные запятыми и переносами строк
            if isinstance(skills_str, str):
                skills_list = skills_str.replace('\n', ',').replace(';', ',').split(',')
                skills_list = [skill.strip() for skill in skills_list if skill.strip()]

                for skill in skills_list:
                    if year not in skills_by_year:
                        skills_by_year[year] = {}
                    if skill not in skills_by_year[year]:
                        skills_by_year[year][skill] = 0
                    skills_by_year[year][skill] += 1

        # Оставляем топ-20 навыков для каждого года и сортируем
        sorted_top_skills = {year: dict(sorted(counts.items(), key=lambda item: item[1], reverse=True)[:20]) for
                             year, counts in skills_by_year.items()}

        # Сохраняем в модель Top_skills
        for year, skills in sorted_top_skills.items():
            Top_skills.objects.create(year=year, skills_list=skills)
