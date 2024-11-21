from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse
from django_jalali.db import models as j
from account.models import User


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to='photos/category', blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_url(self):
        return reverse('complexes_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name


class Complex(models.Model):
    supervisor = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    complex_name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='complex_name', unique=True, always_update=True)
    complex_description = models.TextField(blank=True, max_length=700)
    complex_img = models.ImageField(upload_to='photos/complexes/', blank=True,null=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    area = models.IntegerField()
    price_variation = models.BooleanField(default=False)
    price = models.IntegerField()
    Address = models.CharField(max_length=500)
    city = models.CharField(max_length=255)
    neighborhood = models.CharField(max_length=255)
    guards_count = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    session_long = models.CharField(max_length=255)
    close_days = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)

    def get_url(self):
        return reverse('complex_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.complex_name


class Session(models.Model):
    complex = models.ForeignKey(Complex, on_delete=models.CASCADE)
    date = j.jDateField()
    time = models.TimeField()
    session_price = models.IntegerField()
    is_available = models.BooleanField(default=True)
    is_reserved = models.BooleanField(default=False)

    def __str__(self):
        return self.complex.complex_name
