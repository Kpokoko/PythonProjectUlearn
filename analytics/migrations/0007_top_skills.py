# Generated by Django 5.1.4 on 2024-12-31 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0006_alter_salary_by_city_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Top_skills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('skills_list', models.JSONField()),
            ],
            options={
                'verbose_name_plural': 'top_skills',
                'db_table': 'top_skills',
            },
        ),
    ]
