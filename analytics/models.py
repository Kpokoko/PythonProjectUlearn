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
