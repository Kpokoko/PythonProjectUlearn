from django.core.management.base import BaseCommand
import matplotlib.pyplot as plt
import numpy as np
from analytics.models import Salary_by_year, Top_skills


class Command(BaseCommand):
    def handle(self, *args, **options):
        raw_data = Salary_by_year.objects.all()
        top_skills = Top_skills.objects.all()

        unique_years = raw_data.values_list('year', flat=True).distinct()

        for year in unique_years:
            data = {}
            skills_frequency = top_skills.filter(year=year).values_list('skills_list', flat=True)

            if skills_frequency:
                top_skills_dict = skills_frequency[0]
                for skill, frequency in top_skills_dict.items():
                    data[skill] = frequency

                names = ['Частота навыка', f'Частотность популярных навыков в {year} году']

                fig, ax = plt.subplots()  # Увеличим размер графика
                self.generate_vertical_graph(data, ax, names)

                fig.tight_layout()
                plt.savefig(f'analytics/static/img/graphs/top_skills_{year}.png')
                plt.show()

    def generate_vertical_graph(self, stats, ax, names):
        """
        Генерирует вертикальный график
        :param stats: обработанные входные данные
        :param ax: полотно для рисования графика
        :param names: подписи
        """
        x = np.arange(len(stats))  # Создание массива индексов
        skills = list(stats.keys())
        values = list(stats.values())

        ax.bar(x, values, label=names[0])
        ax.set_title(names[1], fontsize=16)
        ax.set_xticks(x)
        ax.set_xticklabels(skills, fontsize=8, rotation=70, ha='right')  # Правильное выравнивание меток
        ax.tick_params(axis='y', labelsize=10)
        ax.legend(fontsize=10)
        ax.grid(axis='y')
