# Generated by Django 3.1.6 on 2021-04-12 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_one', '0006_auto_20210412_1609'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.BooleanField(choices=[(True, 'Present'), (False, 'Absent')])),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_one.course')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_one.studentinfo')),
            ],
        ),
    ]