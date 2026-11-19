
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Электронная почта'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Пользователь с такой почтой уже зарегистрирован.'
            )

        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя'
    )

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput
    )


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='Введите ваш Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'example@mail.ru'
        })
    )


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput()
    )

    confirm_password = forms.CharField(
        label='Подтвердите пароль',
        widget=forms.PasswordInput()
    )

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают.')

        return cleaned_data
