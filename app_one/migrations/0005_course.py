# Generated by Django 3.1.6 on 2021-04-12 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_one', '0004_auto_20210407_1556'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_name', models.CharField(max_length=20)),
                ('course_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
            ],
        ),
    ]