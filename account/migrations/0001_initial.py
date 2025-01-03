# Generated by Django 5.0.6 on 2024-06-21 16:39

import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('national_code', models.CharField(max_length=10, unique=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('zone', models.CharField(blank=True, max_length=255, null=True)),
                ('delivery_date', models.DateField(blank=True, null=True)),
                ('sheba_number', models.CharField(blank=True, max_length=255, null=True)),
                ('sheba_name', models.CharField(blank=True, max_length=255, null=True)),
                ('income_settlement', models.IntegerField(blank=True, choices=[(1, 'روزانه'), (2, 'هفتگی'), (3, '15 روزه'), (4, 'ماهانه')], default=1, null=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_superadmin', models.BooleanField(default=False)),
                ('is_supervisor', models.BooleanField(default=False)),
                ('role', models.IntegerField(choices=[(1, 'مدیر کل'), (2, 'ادمین'), (3, 'مشتری'), (4, 'سوپروایزر')], default=3)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]
