from django.contrib import admin
from .models import Reserve, Payment


# Register your models here.

class ReserveAdmin(admin.ModelAdmin):
    list_display = ['reserve_number', 'full_name', 'phone', 'reserve_total', 'status', 'is_reserved', 'created_at']
    list_filter = ['status', 'is_reserved']
    search_fields = ['reserve_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 20


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'pay_date']
    list_per_page = 20


admin.site.register(Reserve, ReserveAdmin)
admin.site.register(Payment, PaymentAdmin)