
from django.contrib import admin
from .models import (
    User,
    CollectionPoint,
    WasteType,
    Submission,
    PointsTransaction,
    PasswordResetToken,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'full_name', 'role', 'is_active')
    search_fields = ('email', 'full_name')
    list_filter = ('role', 'is_active')


@admin.register(CollectionPoint)
class CollectionPointAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'is_active')
    search_fields = ('name', 'address')
    list_filter = ('is_active',)


@admin.register(WasteType)
class WasteTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'point', 'waste_type', 'quantity_kg', 'status')
    list_filter = ('status',)


@admin.register(PointsTransaction)
class PointsTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'submission', 'amount', 'transaction_type')


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'expires_at', 'used_at')
