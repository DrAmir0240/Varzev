from django import forms

from complex.models import Complex, Category


class ComplexForm(forms.ModelForm):
    class Meta:
        model = Complex
        fields = ['complex_name', 'complex_description', 'complex_img', 'category', 'area', 'price_variation', 'price',
                  'Address', 'session_long', 'close_days', 'city', 'neighborhood', 'guards_count', 'start_time',
                  'end_time']

