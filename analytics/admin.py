from django.contrib import admin
from .models import *

admin.site.register(Vacancy)
admin.site.register(Salary_by_year)
admin.site.register(Vacancies_by_year)
admin.site.register(Currency)
admin.site.register(Vacancies_by_city)
admin.site.register(Salary_by_city)
admin.site.register(Top_skills)
