# Generated by Django 5.0.6 on 2024-06-22 13:05

import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('complex', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='date',
            field=django_jalali.db.models.jDateField(),
        ),
    ]
