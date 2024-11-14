# Importing necessary module and model
from captcha.fields import CaptchaField
from django import forms  # Module for defining forms
from .models import User  # Importing model for Account


# Form for user registration
class RegistrationForm(forms.ModelForm):
    """
    Form for user registration.

    Attributes:
        password (CharField): Field for entering password.
        confirm_password (CharField): Field for confirming password.
    """

    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    captcha = CaptchaField()

    class Meta:
        """
        Meta class for RegistrationForm.

        Specifies the model and fields to be used in the form.
        """
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'password']

    def clean(self):
        """
        Validates the form data.

        Raises:
            forms.ValidationError: If the passwords do not match.
        """
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password does not match.")

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        # Ensure it's a string
        if isinstance(phone_number, tuple):
            phone_number = phone_number[0]
        return phone_number


class SupervisorRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['phone_number', 'national_code', 'email', 'first_name', 'last_name', 'birth_date', 'city', 'zone',
                  'delivery_date', 'sheba_number', 'sheba_name', 'income_settlement', 'password']

    def clean(self):
        """
        Validates the form data.

        Raises:
            forms.ValidationError: If the passwords do not match.
        """
        cleaned_data = super(SupervisorRegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password does not match.")

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        # Ensure it's a string
        if isinstance(phone_number, tuple):
            phone_number = phone_number[0]
        return phone_number
