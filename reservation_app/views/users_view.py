from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from reservation_app.repositories.user_repository import UserRepository
from reservation_app.utils import jwt
from reservation_app.utils.custom_decorators import is_authenticated

from .base_view import BaseView


class UsersView(BaseView):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)



        
    
    