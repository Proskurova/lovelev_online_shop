from django import forms
from phonenumber_field.formfields import PhoneNumberField, RegionalPhoneNumberWidget


class QuestionUserForm(forms.Form):
    username = forms.CharField(label='Ваше имя', max_length=100, widget=forms.TextInput(
        attrs={'class': 'font-400-12 question_form_input', 'placeholder': 'Иванов Иван Иванович'}))
    phone = PhoneNumberField(label='Номер телефона', max_length=70, widget=RegionalPhoneNumberWidget(
        attrs={'class': 'font-400-12 question_form_input', 'placeholder': 'Введите ваши данные в формате +375000000000'}))
    question = forms.CharField(label='Ваш вопрос', max_length=2000, widget=forms.Textarea(
        attrs={'class': 'font-400-12 question_form_input_text', 'placeholder': 'Напишите ваш вопрос...'}))
    approval = forms.BooleanField(required=True, initial=False, label='Я принимаю условия')
