from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid


# Create your models here.
class Faculty(models.Model):
    name = models.CharField(max_length=50)


class Cathedra(models.Model):
    name = models.CharField(max_length=50)
    faculty_id = models.ForeignKey('Faculty', on_delete=models.CASCADE, related_name='cathedras')


class Specialty(models.Model):
    name = models.CharField(max_length=50)
    cathedra_id = models.ForeignKey('Cathedra', on_delete=models.CASCADE, related_name='specialties')


class StudyGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    TYPES_CHOICES = [
        ('SP', 'специалитет'),
        ('BA', 'бакалавриат'),
        ('MA', 'магистратура'),
    ]
    current_name = models.CharField(max_length=3)
    specialty_id = models.ForeignKey('Specialty', on_delete=models.CASCADE, related_name='study_groups')
    form_of_study = models.CharField(max_length=2, choices=TYPES_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)


class User(AbstractUser):
    # Дефолтные поля:
    # username
    # email
    # first_name
    # last_name
    # date_joined
    # last_login
    # is_active
    # is_staff
    # is_superuser
    # groups - связь
    # user_permissions - связь
    # Кастомные поля:
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    middle_name = models.CharField(max_length=50, default='')
    date_of_birth = models.DateField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)


class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    study_group_id = models.ForeignKey('StudyGroup', on_delete=models.CASCADE, related_name='students')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='students')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)


class Rating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student_id = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='ratings')
    # Пример: values = {'Физика': {'current': 25, 'max': 50}, 'САПР': {'current': 12, 'max': 30}}
    values = JSONField(default=dict)
    checkpoint_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
