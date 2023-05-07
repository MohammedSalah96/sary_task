import datetime
from functools import wraps

from rest_framework import status
from rest_framework.response import Response

from reservation_app.repositories.user_repository import UserRepository
from reservation_app.utils import jwt


def is_authenticated(allowed_roles=[]):
    def decorator(view_function):
        @wraps(view_function)
        def wrapped(request, *args, **kwargs):
            if not 'Authorization' in request.headers:
                return Response({"message": "Authorization token not provided"}, status=status.HTTP_401_UNAUTHORIZED)
            token = jwt.get_payload(request.headers.get('Authorization'))
            if not token:
                return Response({"message": "Invalid Authorization token"}, status=status.HTTP_401_UNAUTHORIZED)
            
            if token.get('exp') < int(datetime.datetime.now().timestamp()):
                return Response({"message": "Expired Authorization token"}, status=status.HTTP_401_UNAUTHORIZED)
            
            user = UserRepository.auth_user_check()
            if not user:
                return Response({"message": "User is not found"}, status=status.HTTP_401_UNAUTHORIZED)
           
            if allowed_roles and user.role not in allowed_roles:
                return Response({"message": "You are not permitted to perform this action"}, status=status.HTTP_403_FORBIDDEN)
            
            return view_function(request, *args, **kwargs)

        return wrapped
    return decorator