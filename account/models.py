import json

import requests
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
import random


class Roles(models.IntegerChoices):
    SUPER_USER = (1, "مدیر کل")
    ADMIN = (2, "ادمین")
    USER = (3, "مشتری")
    SUPERVISOR = (4, "سوپروایزر")


class Settlements(models.IntegerChoices):
    daily = (1, "روزانه")
    weekly = (2, "هفتگی")
    fifteen_days = (3, "15 روزه")
    monthly = (4, "ماهانه")


class UserManager(BaseUserManager):
    def create_user(self, phone_number, first_name, last_name, password=None):
        if not phone_number:
            raise ValueError("User must have a phone number.")

        user = self.model(
            phone_number=phone_number,
            last_name=last_name,
            first_name=first_name

        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, first_name, last_name, password):
        user = self.create_user(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.role = Roles.SUPER_USER
        user.save(using=self._db)
        return user

    def create_supervisor(self, phone_number, national_code, email, first_name, last_name, birth_date, city, zone,
                          delivery_date, sheba_number, sheba_name, income_settlement=Settlements.daily, password=None):
        if not phone_number:
            raise ValueError("Supervisor must have a phone number.")
        if not email:
            raise ValueError("Supervisor must have an email address.")
        if not national_code:
            raise ValueError("Supervisor must have a national code.")

        supervisor = self.model(
            phone_number=phone_number,
            national_code=national_code,
            email=email,
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            city=city,
            zone=zone,
            delivery_date=delivery_date,
            sheba_number=sheba_number,
            sheba_name=sheba_name,
            income_settlement=income_settlement
        )
        supervisor.set_password(password)
        supervisor.is_supervisor = True
        supervisor.save(using=self._db)
        return supervisor


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True)
    national_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    zone = models.CharField(max_length=255, blank=True, null=True)
    delivery_date = models.CharField(max_length=10, blank=True, null=True)
    sheba_number = models.CharField(max_length=255, blank=True, null=True)
    sheba_name = models.CharField(max_length=255, blank=True, null=True)
    income_settlement = models.IntegerField(choices=Settlements.choices, default=Settlements.daily, blank=True,
                                            null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)
    balance = models.CharField(max_length=255, blank=True, null=True)
    score = models.CharField(max_length=255, blank=True, null=True)
    role = models.IntegerField(choices=Roles.choices, default=Roles.USER)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.phone_number

    def full_name(self):
        return f"{self.first_name}-{self.last_name}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def send_otp(self):
        # Generate a 6-digit OTP
        otp = str(random.randint(100000, 999999))

        api = '7sR4Ia89PheQ3KAdKuqegM-HbBEN0vIQtt7Mvw_QQ6A='
        url = "https://api2.ippanel.com/api/v1/sms/pattern/normal/send"

        try:
            payload = json.dumps({
                "code": "dobc7wlhaxx361a",
                "sender": "+983000505",
                "recipient": f"{self.phone_number}",
                "variable": {
                    "OTP": otp,
                }
            })
            headers = {
                'apikey': f'{api}',
                'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)

            # Check if the request was successful
            if response.status_code == 200:
                return otp  # Return the generated OTP instead of expecting it from the response
            else:
                return None

        except Exception as e:
            print(f'Exception: {e}')
            return None
