from django.db import models

from .base_model import BaseModel
from .table import Table
from .user import User


class Reservation(BaseModel):
    class Meta:
        db_table = 'reservations'
    reserved_at = models.DateField(auto_now_add=True)
    starting_time = models.TimeField()
    ending_time = models.TimeField()
    table = models.ForeignKey(Table, on_delete= models.PROTECT, related_name='table', db_column='table_id')
    created_by = models.ForeignKey(User, on_delete= models.PROTECT, default=None, related_name='reserved_by', db_column='created_by', blank=True)