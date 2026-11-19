
from datetime import timedelta

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('user', 'Пользователь'),
        ('admin', 'Администратор'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user'
    )

    def __str__(self):
        return f'{self.user.username} — {self.get_role_display()}'


class PasswordResetToken(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reset_tokens'
    )

    token_hash = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=30)
        super().save(*args, **kwargs)

    def is_valid(self):
        return not self.is_used and self.expires_at > timezone.now()

    def __str__(self):
        return f'Токен восстановления: {self.user.username}'
