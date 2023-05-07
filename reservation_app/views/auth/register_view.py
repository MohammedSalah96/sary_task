from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from reservation_app.serializers.user_serializer import UserSerializer
from reservation_app.utils.custom_decorators import is_authenticated


class AdminsView(APIView):
    def post(self, request):
        try:
            data = UserSerializer(data=request.data)
            if not data.is_valid():
                return Response({'errors': data.errors}, status=status.HTTP_400_BAD_REQUEST)
            data.save()
            return Response({'message': 'Added Succefully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
           return Response({'message': 'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)

class EmployeesView(APIView):
    @method_decorator(is_authenticated(allowed_roles=['Admin']))
    def post(self, request):
        try:
            request.data._mutable = True
            request.data.update({'role': 'Employee'})
            data = UserSerializer(data=request.data)
            if not data.is_valid():
                return Response({'errors': data.errors}, status=status.HTTP_400_BAD_REQUEST)
            data.save()
            return Response({'message': 'Added Succefully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
           return Response({'message': 'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)   