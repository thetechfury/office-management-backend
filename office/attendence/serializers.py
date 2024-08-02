import datetime
from rest_framework import serializers
from .models import Break,Shift,UserShift,Attendence
from datetime import datetime, timedelta

class BreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = Break
        fields = ['id', 'shift', 'start_time', 'end_time', 'duration']
        extra_kwargs = {
            'duration':{'read_only':True}
        }



class ShiftSerializer(serializers.ModelSerializer):
    breaks = BreakSerializer(many=True, read_only=True)
    duration = serializers.SerializerMethodField()

    def get_duration(self, obj):
        start = datetime.combine(datetime.today(), obj.start_time)
        end = datetime.combine(datetime.today(), obj.end_time)
        duration = end - start
        return duration if duration >= timedelta(0) else timedelta(0)

    class Meta:
        model = Shift
        fields = ['id', 'name', 'description', 'start_time', 'end_time','duration', 'breaks']


class UserShiftSerializer(serializers.ModelSerializer):
    shift = ShiftSerializer(read_only=True)
    class Meta:

        model = UserShift
        fields = ['id', 'user', 'shift', 'date']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date'] = instance.date.strftime('%d %b %Y')
        return representation


class AttendenceSerializer(serializers.ModelSerializer):
    def check_is_attendence_already_marked(self):
        current_date = datetime.datetime.today().date()
        object = Attendence.objects.filter(user = self.context['request'].user,date__date = current_date)
        return object

    def check_clock_out_exist(self,objects):
        for object in objects:
            if object.operation == "clock_out":
                return True
        return False

    def get_user_shift(self, obj):
        user_shift = obj.get_user_shift()
        if user_shift:
            return {
                'shift': user_shift.shift.name
            }
        return None

    user_shift = serializers.SerializerMethodField()
    class Meta:
        model = Attendence
        fields = ['user', 'date', 'operation', 'user_shift']
    def get_extra_kwargs(self,*args,**kwargs):
        extra_kwargs = super().get_extra_kwargs(*args,**kwargs)
        extra_kwargs['id'] = {'read_only' : True}
        extra_kwargs['user'] = {'read_only' : False}
        return extra_kwargs
        # if not self.context['request'].user.role == 'admin':
        #     extra_kwargs['date'] = {'read_only': True}
        #     extra_kwargs['user'] = {'read_only': True}
        # return extra_kwargs

    def create(self, validated_data):
        # check is user already clock in our clock out for current date
        is_already_marked = self.check_is_attendence_already_marked()
        current_user = self.context['request'].user
        operation = validated_data.pop('operation')
        if validated_data.get("user"):
            current_user = validated_data.pop("user")
        if not is_already_marked:
            if operation == "clock_out":
                raise serializers.ValidationError("You can't clock out until first you clock in")
            else:
                return Attendence.objects.create(**validated_data,user = current_user,operation = operation)
        else:
            # check if user already clock out
            already_clock_out = self.check_clock_out_exist(is_already_marked)
            if not already_clock_out and operation == 'clock_out':
                return Attendence.objects.create(**validated_data, user=current_user,operation = operation)
            elif operation == "clock_in":
                raise serializers.ValidationError("you already clock_in")
            else:
                raise serializers.ValidationError("you already clock_in and clock out")


