from datetime import datetime, timedelta

from django.shortcuts import render
from analytics.models import *
import requests


def index(request):
    return render(request, 'index.html')


def full_info(request):
    salaries_by_year = Salary_by_year.objects.all()
    vacancies_by_year = Vacancies_by_year.objects.all()
    salaries_by_city = Salary_by_city.objects.all()
    vacancies_by_city = Vacancies_by_city.objects.all()
    top_skills = Top_skills.objects.all()
    return render(request, 'full_info.html',
                  {'salaries_by_year': salaries_by_year, 'vacancies_by_year': vacancies_by_year,
                   'salaries_by_city': salaries_by_city, 'vacancies_by_city': vacancies_by_city,
                   'top_skills': top_skills})


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


def top_skills(request):
    top_skills = Top_skills.objects.all()
    return render(request, 'top_skills.html', {'top_skills': top_skills})


def load_vacancies(keywords):
    api = 'https://api.hh.ru/vacancies'
    query = ' OR '.join(f'{keyword}' for keyword in keywords)
    query = 'NAME:(' + query + ')'
    time = datetime.now()
    time_limit = time - timedelta(days=1)
    date_from = time_limit.isoformat()
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


currencies_names = {
    'AZN': 'манат',
    'BYR': 'белорусских рублей',
    'EUR': 'евро',
    'GEL': 'грузинских лари',
    'KGS': 'кыргызских сомов',
    'KZT': 'тенге',
    'RUR': 'рублей',
    'UAH': 'гривен',
    'USD': 'долларов',
    'UZS': 'узбекских сум'
}


def get_salary(salary):
    salary_from = salary.get('from') or ''
    salary_to = salary.get('to') or ''
    currency_id = salary.get('currency') or ''
    currency_name = ''
    if currency_id:
        currency_name = currencies_names[currency_id]
    if salary_from and salary_to:
        return str(salary_from) + ' - ' + str(salary_to) + ' ' + currency_name
    elif salary_from:
        return 'от ' + str(salary_from) + ' ' + currency_name
    elif salary_to:
        return 'до ' + str(salary_to) + ' ' + currency_name
    else:
        return 'не указан'


def last_vacancies(request):
    keywords = ['Системный администратор', 'system admin', 'сисадмин', 'сис админ', 'системный админ',
                'cистемный админ',
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
        skills_list = ", ".join([skill['name'] for skill in details.get('key_skills', [])])
        if not skills_list:
            skills_list = 'не указаны'

        detailed_vacancies.append({
            'title': details.get('name'),
            'description': details.get('description', 'пусто'),  # Пусто если нет описания
            'skills': skills_list,
            'company': details.get('employer', {}).get('name', 'неизвестна'),  # заглушка если нет компании
            'salary': get_salary(salary),
            'region': details.get('area', {}).get('name', 'не указан'),  # заглушка если нет региона
            'published_at': details.get('published_at')
        })

    return render(request, 'last_vacancies.html', {'vacancies': detailed_vacancies})
