from rest_framework import serializers
from .models import Break,Shift,UserShift
class BreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = Break
        fields = ['id', 'shift', 'start_time', 'end_time', 'duration']
        extra_kwargs = {
            'duration':{'read_only':True}
        }



class ShiftSerializer(serializers.ModelSerializer):
    breaks = BreakSerializer(many=True, read_only=True)

    class Meta:
        model = Shift
        fields = ['id', 'name', 'description', 'start_time', 'end_time', 'breaks']


class UserShiftSerializer(serializers.ModelSerializer):
    total_working_hours = serializers.SerializerMethodField()

    class Meta:
        model = UserShift
        fields = ['id', 'user', 'shift', 'date', 'total_working_hours']

    def get_total_working_hours(self, obj):
        return obj.get_total_working_hours().total_seconds() / 3600  # converting to hours

