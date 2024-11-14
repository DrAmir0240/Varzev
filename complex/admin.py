from django.contrib import admin

from complex.models import Session, Complex, Category


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')


class ComplexAdmin(admin.ModelAdmin):
    list_display = ('complex_name', 'supervisor', 'is_active')


class SessionAdmin(admin.ModelAdmin):
    list_display = ('complex', 'date', 'time', 'is_available', 'is_reserved')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Complex, ComplexAdmin)
admin.site.register(Session, SessionAdmin)
