import datetime

from django.db.models import Q

from reservation_app.models.reservation import Reservation
from reservation_app.models.table import Table

from .base_repository import BaseRepository


class ReservationRepository(BaseRepository):
    
    model = Reservation
    
    @classmethod
    def available_slots(cls, filters):
        reservations = cls.model.objects.filter(table=filters.get('table'))
        if filters.get('table'):
            reservations = reservations.filter(table=filters.get('table'))
        if filters.get('from_date'):
            reservations = reservations.filter(reserved_at__gte = filters.get('from_date'))
        if filters.get('to_date'):
            reservations = reservations.filter(reserved_at__lte = filters.get('to_date'))
        return reservations
    
    @classmethod
    def all(cls, filters):
        reservations = cls.model.objects.prefetch_related('table').all()
        if filters.get('table'):
            reservations = reservations.filter(table=filters.get('table'))
        if filters.get('from_date'):
            reservations = reservations.filter(reserved_at__gte = filters.get('from_date'))
        if filters.get('to_date'):
            reservations = reservations.filter(reserved_at__lte = filters.get('to_date'))
        return reservations
             
    @classmethod
    def create(cls, **kwargs):
        table = cls.model(**kwargs)
        table.created_by = cls.auth_user()
        table.save()
        return table
    
    @classmethod
    def is_reserved(cls, data):
        return cls.model.objects.filter(table = data.get('table')) \
        .filter(reserved_at = datetime.datetime.today()) \
        .filter((Q(starting_time__gte=data.get('starting_time')) & Q(starting_time__lt=data.get('ending_time')))
            | (Q(ending_time__gt=data.get('starting_time')) & Q(ending_time__lte=data.get('ending_time')))
            | (Q(starting_time__gte=data.get('starting_time')) & Q(ending_time__lt=data.get('starting_time')))
            | (Q(starting_time__lte=data.get('starting_time')) & Q(ending_time__gte=data.get('ending_time')))
            ).first()
    
    @classmethod
    def within_working_hours(cls, data):
        return data.get('starting_time') >= datetime.time(12,0) and data.get('ending_time') <= datetime.time(23, 59)
    
    @classmethod
    def today_reservation(cls, data):
        order_by = 'starting_time'
        if data.get('order_by_date') == 'desc':
            order_by = '-starting_time'
        return cls.model.objects.prefetch_related('table').filter(reserved_at = datetime.datetime.today()).order_by(order_by)
    
    @classmethod
    def get_tables_reservations(cls, tables):
        return cls.model.objects.filter(table_id__in = tables).filter(reserved_at=cls.now.date()).order_by('table_id', 'starting_time')
        
    