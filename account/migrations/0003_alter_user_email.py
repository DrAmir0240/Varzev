# Generated by Django 5.0.6 on 2024-06-21 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_user_email_alter_user_national_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
