from django.db import models
from account.models import User
from complex.models import Session


# Create your models here.

class Reserve(models.Model):
    STATUS = (
        ('در انتظار پرداخت', 'در انتظار پرداخت'),
        ('تایید شده', 'تایید شده'),
        ('کنسل شده', 'کنسل شده'),
        ('تاریخ پرداخت گدشته', 'تاریخ پرداخت گذشته'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="RESERVES")
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    reserve_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    reserve_note = models.CharField(max_length=100, blank=True, null=True)
    reserve_total = models.IntegerField()
    status = models.CharField(max_length=25, choices=STATUS, default='در انتظار پرداخت')
    ip = models.CharField(max_length=20, blank=True)
    is_reserved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"رزرو سانس روز {self.session.date} و تاریخ {self.session.time} سالن {self.session.complex}"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    reserve = models.OneToOneField(Reserve, on_delete=models.CASCADE)
    amount = models.CharField(max_length=10)
    pay_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"پرداخت با شماره {self.id} برای کاربر {self.user}"