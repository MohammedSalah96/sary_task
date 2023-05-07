from rest_framework import serializers

from reservation_app.models.user import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'employee_no', 'role', 'password')
        write_only = ['password', 'role']
        extra_kwargs = {
            'name': {
                'error_messages': {
                    'blank': 'Name is required'
                    }
                },
            'employee_no': {
                'error_messages': {
                    'blank': 'Employee No is required'
                    }
                },
            'password': {
                'error_messages': {
                    'blank': 'Password is required'
                    }
                },
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user 

        