from django import forms
from django.core.exceptions import ValidationError

from .models import Order
from phonenumber_field.formfields import PhoneNumberField, RegionalPhoneNumberWidget


class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['first_name', 'phoneNumber', 'email', 'city', 'delivery', 'address', 'comment', 'paymentMethod']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'font-400-12 cart_form_input', 'placeholder': 'Иванов Иван Иванович'}),
            'address': forms.TextInput(attrs={'class': 'font-400-12 cart_form_input', 'placeholder': 'Введите ваш адрес'}),
            'email': forms.EmailInput(attrs={'class': 'font-400-12 cart_form_input', 'placeholder': 'Введите ваши данные'}),
            'city': forms.TextInput(attrs={'class': 'font-400-12 cart_form_input', 'placeholder': 'Ваш город'}),
            'comment': forms.TextInput(attrs={'class': 'font-400-12 cart_form_input', 'placeholder': 'Введите ваш комментарий'}),
            'phoneNumber': RegionalPhoneNumberWidget(attrs={'class': 'font-400-12 cart_form_input', 'placeholder': 'Введите ваши данные'})
        }

    def clean(self):
        pass

