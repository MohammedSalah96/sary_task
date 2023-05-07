import datetime
from datetime import timezone

from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from reservation_app.models.reservation import Reservation
from reservation_app.models.table import Table
from reservation_app.repositories.reservation_repository import \
    ReservationRepository
from reservation_app.repositories.table_repository import TableRepository
from reservation_app.serializers.reservation_serializer import \
    ReservationSerializer
from reservation_app.utils.custom_decorators import is_authenticated

from .base_view import BaseView


class ReservationsView(BaseView, PageNumberPagination):
    
    @method_decorator(is_authenticated(allowed_roles=['Admin']))
    def get(self, request):
        try:
            reservations = ReservationSerializer(self.paginate_queryset(ReservationRepository.all(request.query_params), request), many=True).data
            return Response({'data': reservations})
        except Exception as e:
            if isinstance(e, NotFound):
                return Response({'data': []})
            return Response({'message': 'Something went wrong!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
    
    
    @method_decorator(is_authenticated(allowed_roles=['Admin']))
    def post(self, request):
        try:
            table = TableRepository.get_by(number=request.data.get('table'))
            if not table:
                return Response({'message': 'Invalid Table No'}, status=status.HTTP_404_NOT_FOUND)
            
            request.data._mutable = True
            request.data.update({'table': 5})
            reservation = ReservationSerializer(data=request.data)
            if not reservation.is_valid():
                return Response({'errors': reservation.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            if not ReservationRepository.within_working_hours(reservation.validated_data):
                return Response({'message': 'Reservations are not possible outside of working hours', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
            
            if ReservationRepository.is_reserved(reservation.validated_data):
                return Response({'message': 'This time slot is not availabe now', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
            reservation = ReservationSerializer(ReservationRepository.create(**reservation.validated_data)).data
            return Response({'message': 'Created Successfully', 'data': reservation}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': 'Something went wrong!', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
        
        
class ReservationDetailsView(BaseView):
    
    @method_decorator(is_authenticated(allowed_roles=['Admin']))
    def delete(self, request, id):
        try:
            reservation = ReservationRepository.get(id)
            if not reservation:
                return Response({'message': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
            ReservationRepository.delete(reservation)
            return Response({'message': 'Deleted Successfully'})
        except Exception as e:
            return Response({'message': 'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)


class ReservationSlotsView(BaseView):
    
    def _get_available_time_slots(self, tables, reservations):
        now = datetime.datetime.now()
        end_of_day = now.replace(hour=23, minute=59, second=0, microsecond=0)
        table_time_slots_map = {}
        for table in tables:
            table_reservations = reservations.filter(table_id = table)
            table_time_slots_map.setdefault(table, {'table_no':table, 'time_slots':[]})
            if not table_reservations:
                table_time_slots_map[table]['time_slots'].append({
                    now.strftime("%I:%M %p") +' - '+ end_of_day.strftime("%I:%M %p")
                })
            else:
                start = now.replace(second=0)
                for reservation in table_reservations:
                    hours, muintes = reservation.starting_time.hour, reservation.starting_time.minute
                    slot_begining = datetime.datetime.now().replace(hour=hours, minute=muintes, second=0, microsecond=0)
                    if start < slot_begining:
                        table_time_slots_map[reservation.table_id]['time_slots'].append(start.strftime("%I:%M %p") + ' - ' + reservation.starting_time.strftime("%I:%M %p"))
                    hours, muintes = reservation.ending_time.hour, reservation.ending_time.minute
                    start = datetime.datetime.now().replace(hour=hours, minute=muintes, second=0, microsecond=0)
                else:
                    if end_of_day > start:
                        table_time_slots_map[reservation.table_id]['time_slots'].append(start.strftime("%I:%M %p") + ' - ' + end_of_day.strftime("%I:%M %p"))
            if not table_time_slots_map[reservation.table_id]['time_slots']:
                table_time_slots_map.pop(table)
        if table_time_slots_map:
            return table_time_slots_map.values()
        return []
        
        
    @method_decorator(is_authenticated(allowed_roles=['Admin', 'Employee']))
    def get(self, request):
        try:
            num_of_guests = request.query_params.get('num_of_guests')
            
            if not num_of_guests:
                return Response({"message": "Please Enter the number of guests."}, status=status.HTTP_400_BAD_REQUEST)
            
            num_of_guests = int(num_of_guests)
            
            tables = TableRepository.get_tables_for_guests(num_of_guests)
            if not tables:
                return Response({"message": "Number of guests exceeds maximum table size."}, status=status.HTTP_400_BAD_REQUEST)
            
            reservations = ReservationRepository.get_tables_reservations(tables)
            return Response({'data': self._get_available_time_slots(tables, reservations)})
        except Exception as e:
            return Response({'message': 'Something went wrong!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
        

class TodayReservationsView(BaseView, PageNumberPagination):
    
    @method_decorator(is_authenticated(allowed_roles=['Admin', 'Employee']))
    def get(self, request):
        try:
            reservations = ReservationSerializer(self.paginate_queryset(ReservationRepository.today_reservation(request.query_params), request), many=True).data
            return Response({'data': reservations})
        except Exception as e:
            if isinstance(e, NotFound):
                return Response({'data': []})
            return Response({'message': 'Something went wrong!', 'data': []}, status=status.HTTP_400_BAD_REQUEST)