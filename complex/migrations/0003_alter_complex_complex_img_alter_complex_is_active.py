# Generated by Django 5.0.6 on 2024-11-21 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complex', '0002_alter_session_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complex',
            name='complex_img',
            field=models.ImageField(blank=True, null=True, upload_to='photos/complexes/'),
        ),
        migrations.AlterField(
            model_name='complex',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
