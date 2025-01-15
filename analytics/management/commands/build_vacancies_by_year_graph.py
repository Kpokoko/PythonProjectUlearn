from django.core.management import BaseCommand
import matplotlib.pyplot as plt
import numpy as np
from analytics.models import Salary_by_year, Vacancies_by_year
import pandas as pd


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = Vacancies_by_year.objects.all().values('year', 'vacancy_count')
        stats = self.get_salary_stats(data)
        names = ['количество вакансий', 'Уровень количества зарплат по годам']

        fig, ax = plt.subplots()
        self.generate_vertical_graph(stats, ax, names)

        fig.tight_layout()  # Оптимизация расположения графиков
        plt.savefig('analytics\\static\\analytics\\img\\graphs\\vacancies_by_year.png')  # Сохранение графика в PNG файл
        plt.show()  # Отображение графиков

    def get_salary_stats(self, data):
        """
        Преобразование QuerySet в словарь для построения графика
        :param data: QuerySet с данными о вакансиях
        :return: распределение зарплат по годам
        """
        df = pd.DataFrame(data)
        avg_salary_by_year = df.set_index('year')['vacancy_count'].to_dict()
        return avg_salary_by_year  # Возврат распределения зарплат по годам

    def generate_vertical_graph(self, stats, ax, names):
        """
        Генерирует вертикальный график
        :param stats: обработанные входные данные
        :param ax: полотно для рисования графика
        :param names: подписи
        """
        x = np.arange(len(stats))  # Создание массива индексов
        years = list(stats.keys())
        values = list(stats.values())

        ax.bar(x, values, color="#61FF7B", label=names[0])  # Отрисовка столбцов
        ax.set_title(names[1], fontsize=12)  # Установка заголовка диаграммы
        ax.set_xticks(x)  # Установка меток по оси X
        ax.set_xticklabels(years, fontsize=10, rotation=45)  # Настройка меток по оси X
        ax.tick_params(axis='y', labelsize=10)  # Настройка параметров меток по оси Y
        ax.legend(fontsize=10)  # Добавление легенды
        ax.grid(axis='y')  # Добавление сетки по оси Y
