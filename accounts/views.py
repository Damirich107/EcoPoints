
import secrets
import hashlib
from smtplib import SMTPException

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.urls import reverse

from .forms import (
    RegisterForm,
    LoginForm,
    ForgotPasswordForm,
    ResetPasswordForm
)
from .models import UserProfile, PasswordResetToken
from .decorators import role_required


User = get_user_model()


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, role='user')

            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')

            return redirect('profile')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            messages.success(request, 'Вы успешно вошли в систему.')
            return redirect('profile')
    else:
        form = LoginForm(request)

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Вы вышли из аккаунта.')

    return redirect('login')


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')





@role_required(['admin'])
def admin_panel_view(request):
    return render(request, 'accounts/admin_panel.html')


def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email__iexact=email).first()

            if user:
                raw_token = secrets.token_urlsafe(32)
                hashed_token = hashlib.sha256(
                    raw_token.encode()
                ).hexdigest()

                # Деактивируем предыдущие неиспользованные токены
                PasswordResetToken.objects.filter(
                    user=user,
                    is_used=False
                ).update(is_used=True)

                # Создаём новый токен со сроком действия 30 минут
                PasswordResetToken.objects.create(
                    user=user,
                    token_hash=hashed_token
                )

                reset_url = request.build_absolute_uri(
                    reverse(
                        'reset_password',
                        kwargs={'token': raw_token}
                    )
                )

                try:
                    send_mail(
                        'Восстановление пароля EcoPoints',
                        f'Для сброса пароля перейдите по ссылке: {reset_url}',
                        None,
                        [user.email],
                        fail_silently=False
                    )
                except SMTPException as e:
                    print(f'Ошибка отправки письма: {e}')

                    PasswordResetToken.objects.filter(
                        token_hash=hashed_token
                    ).update(is_used=True)

                    messages.error(
                        request,
                        'Произошла ошибка при отправке письма. Попробуйте позже.'
                    )
                    return redirect('forgot_password')

            # Одинаковый ответ для существующего и несуществующего email
            messages.success(
                request,
                'Если аккаунт с таким email существует, письмо отправлено.'
            )
            return redirect('login')

    else:
        form = ForgotPasswordForm()

    return render(
        request,
        'accounts/forgot_password.html',
        {'form': form}
    )


def reset_password_view(request, token):
    hashed_token = hashlib.sha256(token.encode()).hexdigest()

    reset_token = PasswordResetToken.objects.filter(
        token_hash=hashed_token,
        is_used=False
    ).first()

    if not reset_token or not reset_token.is_valid():
        messages.error(
            request,
            'Ссылка недействительна или срок её действия истёк.'
        )
        return redirect('login')

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)

        if form.is_valid():
            user = reset_token.user

            user.set_password(form.cleaned_data['password'])
            user.save()

            # После успешной смены пароля токен становится недействительным
            reset_token.is_used = True
            reset_token.save()

            messages.success(
                request,
                'Пароль успешно изменён. Войдите с новым паролем.'
            )
            return redirect('login')

    else:
        form = ResetPasswordForm()

    return render(
        request,
        'accounts/reset_password.html',
        {'form': form}
    )
