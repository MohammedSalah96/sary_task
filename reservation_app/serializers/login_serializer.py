from django.core.validators import MinLengthValidator
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    employee_no = serializers.CharField(max_length=4, validators=[
        MinLengthValidator(4, 'Employee No has to be 4 characters')
    ], error_messages={'required': 'Employee No is required'})
    password = serializers.CharField(validators=[
        MinLengthValidator(6, 'Password must contain at least 6 characters')
    ], error_messages={'required': 'Password is required'})

        