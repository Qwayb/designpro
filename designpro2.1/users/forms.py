from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=100,
        label='ФИО',
        help_text='Только кириллические буквы, дефис и пробелы',
        widget=forms.TextInput(attrs={'placeholder': 'Введите ваше ФИО'})
    )
    email = forms.EmailField(
        label='Email',
        help_text='Введите валидный email адрес',
        widget=forms.EmailInput(attrs={'placeholder': 'example@mail.com'})
    )
    consent = forms.BooleanField(
        label='Согласие на обработку персональных данных',
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'password1', 'password2', 'consent']
        labels = {
            'username': 'Логин',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля'
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Введите логин'}),
        }
        help_texts = {
            'username': '150 символов или менее. Только латиница и дефис.',
            'password1': 'Пароль должен содержать не менее 8 символов и не должен быть слишком простым.',
        }

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not re.match(r'^[А-Яа-яЁё\s\-]+$', full_name):
            raise ValidationError('ФИО может содержать только кириллические буквы, пробелы и дефисы.')
        return full_name

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z\-]+$', username):
            raise ValidationError('Логин может содержать только латинские буквы и дефисы.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Этот email уже используется.')
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        try:
            validate_password(password)
        except ValidationError as e:
            error_messages = [str(err) for err in e.messages]
            raise ValidationError(error_messages)
        return password

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'autofocus': True}))