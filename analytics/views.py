from django.shortcuts import render
from analytics.models import *


def index(request):
    return render(request, 'index.html')


def demand(request):
    salaries_by_year = Salary_by_year.objects.all()
    vacancies_by_year = Vacancies_by_year.objects.all()
    return render(request, 'demand.html', {'salaries_by_year': salaries_by_year, 'vacancies_by_year': vacancies_by_year})
