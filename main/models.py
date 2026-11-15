
from django.db import models
from django.utils import timezone


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(max_length=150)
    password_hash = models.CharField(max_length=255)
    full_name = models.CharField(max_length=150)
    role = models.CharField(max_length=20, default='user')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'users'
        managed = False

    def __str__(self):
        return self.email


class CollectionPoint(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    working_hours = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'collection_points'
        managed = False

    def __str__(self):
        return self.name


class WasteType(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'waste_types'
        managed = False

    def __str__(self):
        return self.name


class PointWasteType(models.Model):
    point_id = models.BigIntegerField()
    waste_type_id = models.BigIntegerField()
    acceptance_rule = models.TextField(null=True, blank=True)

    pk = models.CompositePrimaryKey('point_id', 'waste_type_id')

    class Meta:
        db_table = 'point_waste_types'
        managed = False


class Submission(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column='user_id')
    point = models.ForeignKey(CollectionPoint, on_delete=models.DO_NOTHING, db_column='point_id')
    waste_type = models.ForeignKey(WasteType, on_delete=models.DO_NOTHING, db_column='waste_type_id')
    quantity_kg = models.DecimalField(max_digits=8, decimal_places=3)
    status = models.CharField(max_length=20, default='pending')
    submitted_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'submissions'
        managed = False


class PointsTransaction(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column='user_id')
    submission = models.ForeignKey(
        Submission,
        on_delete=models.DO_NOTHING,
        db_column='submission_id',
        null=True,
        blank=True
    )
    amount = models.IntegerField()
    transaction_type = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'points_transactions'
        managed = False


class FavoritePoint(models.Model):
    user_id = models.BigIntegerField()
    point_id = models.BigIntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    pk = models.CompositePrimaryKey('user_id', 'point_id')

    class Meta:
        db_table = 'favorite_points'
        managed = False


class PasswordResetToken(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column='user_id')
    token_hash = models.CharField(max_length=64)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'password_reset_token'
        managed = False
