from reservation_app.models.table import Table

from .base_repository import BaseRepository


class TableRepository(BaseRepository):
    
    model = Table
    
    @classmethod
    def get_by(cls, **kwargs):
        return cls.model.objects.filter(**kwargs).first()
    
    @classmethod
    def create(cls, **kwargs):
        table = cls.model(**kwargs)
        table.created_by = cls.auth_user()
        table.save()
        return table
    
    @classmethod
    def get_tables_for_guests(cls, num_of_guests):
        if num_of_guests > cls.all().order_by('-number_of_seats').first().number_of_seats:
            return False
        tables =  cls.model.objects.filter(number_of_seats__gte = num_of_guests).order_by('number_of_seats')
        no_of_seats = tables.first().number_of_seats
        tables = tables.filter(number_of_seats = no_of_seats).values_list('id', flat=True)
        return list(tables)
            
    