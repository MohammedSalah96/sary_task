from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MinLengthValidator
from django.db import models

from .base_model import BaseModel


class User(BaseModel, AbstractBaseUser):
    class Meta:
        db_table = 'users'
    ROLES = [
        ('Admin', 'Admin'),
        ('Employee', 'Employee')
    ]
    name = models.CharField(max_length=255)
    employee_no = models.CharField(max_length=4, unique=True, validators=[
        MinLengthValidator(4, 'Employee No has to be 4 characters')
    ], error_messages={
        "unique": "This Employee No is already exists"
    })
    role = models.CharField(choices=ROLES, default='Admin')
    password = models.CharField(max_length=400, validators=[
        MinLengthValidator(6, 'Password must contain at least 6 characters')
    ])
    is_active = models.IntegerField(default=1)
    
    USERNAME_FIELD = "employee_no"