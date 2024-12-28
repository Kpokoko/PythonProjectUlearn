from django.db import models


class Vacancy(models.Model):
    name = models.CharField(max_length=150)
    key_skills = models.TextField()
    salary_from = models.FloatField(null=True, blank=True)
    salary_to = models.FloatField(null=True, blank=True)
    salary_currency = models.CharField(max_length=5)
    area_name = models.CharField(max_length=50)
    published_at = models.DateTimeField()

    def __str__(self):
        return self.name


class Currency(models.Model):
    date = models.DateField()
    currency_code = models.CharField(max_length=5)
    currency = models.FloatField()

    class Meta:
        unique_together = ('date', 'currency_code')
        db_table = 'currencies'



class Salary_by_year(models.Model):
    avg_salary = models.FloatField()
    year = models.IntegerField()

    class Meta:
        db_table = 'salaries_by_year'

class Vacancies_by_year(models.Model):
    vacancy_count = models.IntegerField()
    year = models.IntegerField()

    class Meta:
        db_table = 'vacancies_by_year'

class Salary_by_city(models.Model):
    avg_salary = models.FloatField()
    area_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'salaries_by_city'


class Vacancies_by_city(models.Model):
    vacancy_count = models.IntegerField()
    vacancy_share = models.FloatField()
    area_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'vacancies_by_city'