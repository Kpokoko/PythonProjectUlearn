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

    class Meta:
        verbose_name_plural = 'Vacancies'
        db_table = 'Vacancies'


class Currency(models.Model):
    date = models.DateField()
    currency_code = models.CharField(max_length=5)
    currency = models.FloatField()

    class Meta:
        unique_together = ('date', 'currency_code')
        db_table = 'currencies'
        verbose_name_plural = 'Currencies'


class Salary_by_year(models.Model):
    avg_salary = models.FloatField()
    year = models.IntegerField()

    class Meta:
        db_table = 'salaries_by_year'
        verbose_name_plural = 'Salaries_by_years'


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
        verbose_name_plural = 'salaries_by_city'


class Vacancies_by_city(models.Model):
    vacancy_count = models.IntegerField()
    vacancy_share = models.FloatField()
    area_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'vacancies_by_city'
        verbose_name_plural = 'vacancies_by_city'


class Top_skills(models.Model):
    year = models.IntegerField()
    skills_list = models.JSONField()

    class Meta:
        db_table = 'top_skills'
        verbose_name_plural = 'top_skills'