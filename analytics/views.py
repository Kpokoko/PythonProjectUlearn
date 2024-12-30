from datetime import datetime, timedelta

from django.shortcuts import render
from analytics.models import *
import requests


def index(request):
    return render(request, 'index.html')


def demand(request):
    salaries_by_year = Salary_by_year.objects.all()
    vacancies_by_year = Vacancies_by_year.objects.all()
    return render(request, 'demand.html',
                  {'salaries_by_year': salaries_by_year, 'vacancies_by_year': vacancies_by_year})


def geography(request):
    salaries_by_city = Salary_by_city.objects.all()
    vacancies_by_city = Vacancies_by_city.objects.all()
    return render(request, 'geography.html',
                  {'salaries_by_city': salaries_by_city, 'vacancies_by_city': vacancies_by_city})


def load_vacancies(keywords):
    api = 'https://api.hh.ru/vacancies'
    query = ' OR '.join(f'{keyword}' for keyword in keywords)
    query = 'NAME:(' + query + ')'
    time = datetime.now()
    time_limit = time - timedelta(days=1)
    date_from = time_limit.isoformat()
    date = datetime.fromisoformat(date_from)
    params = {
        'text': query,
        'date_from': date_from,
        'order_by': 'publication_time',
        'per_page': '10',
    }
    response = requests.get(api, params=params)
    response.raise_for_status()
    return response.json().get('items', [])


def get_vacancy_info(vacancy_id):
    api = f'https://api.hh.ru/vacancies/{vacancy_id}'
    response = requests.get(api)
    response.raise_for_status()
    return response.json()


def get_salary(salary):
    salary_from = salary.get('from') or ''
    salary_to = salary.get('to') or ''
    print(salary)
    currency = salary.get('currency') or 'as'
    if salary_from and salary_to:
        return str(salary_from) + ' - ' + str(salary_to) + ' ' + currency
    elif salary_from:
        return 'От ' + str(salary_from) + ' ' + currency
    elif salary_to:
        return 'До ' + str(salary_to) + ' ' + currency
    else:
        return '0'


def last_vacancies(request):
    keywords = ['Системный администратор', 'system admin', 'сисадмин', 'сис админ', 'системный админ', 'cистемный админ',
            'администратор систем', 'системний адміністратор']
    vacancies = load_vacancies(keywords)
    detailed_vacancies = []

    if not vacancies:
        return render(request, 'last_vacancies.html', {'vacancies': []})

    for vacancy in vacancies:
        details = get_vacancy_info(vacancy['id'])
        if details is None:
            continue
        salary = details.get('salary') or {}

        detailed_vacancies.append({
            'title': details.get('name', 'No title'),  # Default value если нет названия
            'description': details.get('description', 'No description'),  # Default value если нет описания
            'skills': ", ".join([skill['name'] for skill in details.get('key_skills', [])]),
            'company': details.get('employer', {}).get('name', 'Unknown company'),  # Default value если нет компании
            'salary': get_salary(salary),  # Используем пустой словарь если 'salary' нет
            'region': details.get('area', {}).get('name', 'Unknown region'),  # Default value если нет региона
            'published_at': details.get('published_at', 'Unknown date')  # Default value если нет даты публикации
        })

    return render(request, 'last_vacancies.html', {'vacancies': detailed_vacancies})
