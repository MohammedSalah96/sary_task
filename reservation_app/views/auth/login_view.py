from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from reservation_app.repositories.user_repository import UserRepository
from reservation_app.serializers.login_serializer import LoginSerializer
from reservation_app.utils import jwt


class LoginView(APIView):
    def post(self, request):
        try:
            login_credentials = LoginSerializer(data=request.data)
            if not login_credentials.is_valid():
                return Response({'errors': login_credentials.errors}, status=status.HTTP_400_BAD_REQUEST)
            user = UserRepository.check_auth(login_credentials.data)
            if not user:
                return Response({'message': 'Invalid Credentials!'}, status=status.HTTP_401_UNAUTHORIZED)
            token = UserRepository.issue_token(user)
            return Response({'message': 'Welcome back!', **token}, status=status.HTTP_200_OK)
        except Exception as e:
           return Response({'message': 'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)

class RefreshTokenView(APIView):
    def post(self, request):
        try: 
            if not 'Authorization' in request.headers:
                return Response({"message": "Authorization token not provided"}, status=status.HTTP_401_UNAUTHORIZED)

            token = jwt.get_payload(request.headers.get('Authorization'))
            if not token:
                return Response({"message": "Invalid Authorization token"}, status=status.HTTP_401_UNAUTHORIZED)
            
            user = UserRepository.auth_user_check(token.get('id'))
            if not user:
                return Response({"message": "User is not found"}, status=status.HTTP_401_UNAUTHORIZED)
            
            return Response(jwt.generate_token({'id': token.get('id')}))
        except Exception as e:
            return Response({'message': 'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)
        