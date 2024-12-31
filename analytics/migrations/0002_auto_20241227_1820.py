from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE TABLE IF NOT EXISTS salaries_by_year (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                avg_salary FLOAT NOT NULL,
                year INTEGER NOT NULL
            );
            """
        ),
    ]
