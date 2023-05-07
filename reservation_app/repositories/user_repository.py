from reservation_app.models.user import User
from reservation_app.utils import jwt

from .base_repository import BaseRepository


class UserRepository(BaseRepository):
    
    model = User
    
    @classmethod
    def issue_token(cls, user):
        return cls.generate_token(user.id)
    
    @classmethod
    def generate_token(cls, id = None):
        payload = {
            'id': id or cls.auth_user().id
        }
        return jwt.generate_token(payload)
    
    @classmethod
    def check_auth(cls, credentials):
        user = cls.model.objects.filter(is_active = 1).filter(employee_no = credentials.get('employee_no')).first()
        if user:
            if user.check_password(credentials.get('password')):
                return user
        return False
    
    @classmethod
    def auth_user_check(cls, id = None):
        user = cls.model.objects.filter(is_active = 1).filter(id = id or cls.auth_user().id).first();
        return user
    
    
    