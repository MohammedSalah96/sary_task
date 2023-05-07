from rest_framework import serializers

from reservation_app.models.table import Table


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ('id', 'number', 'number_of_seats')
        extra_kwargs = {
            'number': {
                'error_messages': {
                    'blank': 'Table Number is required'
                    }
                },
            'number_of_seats': {
                'error_messages': {
                    'blank': 'Number of seats is required'
                    }
                }
        }

        