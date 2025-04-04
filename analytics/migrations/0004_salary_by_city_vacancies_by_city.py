# Generated by Django 5.1.4 on 2024-12-28 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0003_vacancies_by_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='Salary_by_city',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avg_salary', models.FloatField()),
                ('area_name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'salaries_by_city',
            },
        ),
        migrations.CreateModel(
            name='Vacancies_by_city',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vacancy_count', models.IntegerField()),
                ('vanacy_share', models.FloatField()),
                ('area_name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'vacancies_by_city',
            },
        ),
    ]
