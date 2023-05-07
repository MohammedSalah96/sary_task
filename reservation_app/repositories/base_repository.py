


import datetime

from django.core.exceptions import ObjectDoesNotExist

from reservation_app.middleware.global_request import get_current_request
from reservation_app.models.user import User
from reservation_app.utils import jwt


class BaseRepository:
    model = None
    now = datetime.datetime.now()
    start_of_day = now.replace(hour=12, minute=0, second=0, microsecond=0)
    end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=0)
    
    @classmethod
    def auth_user(cls):
        request = get_current_request()
        token = jwt.get_payload(request.headers.get('authorization'))
        user = None
        if token:
            try:
                user = User.objects.get(pk = token.get('id'))
            except ObjectDoesNotExist:
                pass
        return user
    
    @classmethod
    def get(cls, pk):
        try:
            return cls.model.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return None

    @classmethod
    def create(cls, **kwargs):
        return cls.model.objects.create(**kwargs)

    @classmethod
    def update(cls, instance, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    @classmethod
    def delete(cls, instance):
        instance.delete()

    @classmethod
    def all(cls):
        return cls.model.objects.all()
    
    