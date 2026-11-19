
from functools import wraps

from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

from .models import UserProfile


def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            # Проверяем авторизацию
            if not request.user.is_authenticated:
                return redirect('login')

            # Суперпользователь имеет права администратора
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            # Проверяем роль обычного пользователя
            try:
                user_role = request.user.profile.role
            except UserProfile.DoesNotExist:
                raise PermissionDenied

            if user_role not in allowed_roles:
                raise PermissionDenied

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator
