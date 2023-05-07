from rest_framework import serializers

from reservation_app.models.reservation import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('id', 'reserved_at', 'starting_time', 'ending_time', 'table')
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['starting_time'] = instance.starting_time.strftime("%I:%M %p")
        representation['ending_time'] = instance.ending_time.strftime("%I:%M %p")
        representation['table'] = instance.table.number

        return representation
    
    def validate(self, data):
        if data["starting_time"] > data["ending_time"]:
            raise serializers.ValidationError({"starting_time": "Strating time cannot be greater than Ending time"})
        return super().validate(data)

        