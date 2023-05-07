from django.db.models.deletion import ProtectedError
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response

from reservation_app.repositories.table_repository import TableRepository
from reservation_app.serializers.table_serializer import TableSerializer
from reservation_app.utils.custom_decorators import is_authenticated

from .base_view import BaseView


class TablesView(BaseView):
    @method_decorator(is_authenticated(allowed_roles=['Admin']))
    def get(self, request):
        try:
            tables = TableSerializer(TableRepository.all(), many=True).data
            return Response({'data': tables})
        except Exception as e:
            return Response({'message': 'Something went wrong!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
    
    @method_decorator(is_authenticated(allowed_roles=['Admin']))
    def post(self, request):
        try:
            data = TableSerializer(data=request.data)
            if not data.is_valid():
                return Response({'errors': data.errors}, status=status.HTTP_400_BAD_REQUEST)
            table = TableSerializer(TableRepository.create(**data.validated_data)).data
            return Response({'message': 'Created Successfully', 'data': table}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': 'Something went wrong!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
        
class TableDetailsView(BaseView):
    @method_decorator(is_authenticated(allowed_roles=['Admin']))
    def delete(self, request, id):
        try:
            table = TableRepository.get(id)
            if not table:
                return Response({'message': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
            TableRepository.delete(table)
            return Response({'message': 'Deleted Successfully'})
        except Exception as e:
            if isinstance(e, ProtectedError):
                return Response({'message': 'This table cannot be removed because it has reservations'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)