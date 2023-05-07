from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .base_model import BaseModel
from .user import User


class Table(BaseModel):
    class Meta:
        db_table = 'tables'
    
    number = models.IntegerField(unique=True, error_messages={'unique': 'This Table Number already exists'})
    number_of_seats = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(12)])
    created_by = models.ForeignKey(User, on_delete= models.PROTECT, default=None, related_name='created_by', db_column='created_by', blank=True)
    
    def is_available_for_reservation(self, num_of_guests):
        return self.number_of_seats >= num_of_guests