from rest_framework import serializers
from .models import LeaveApplication
class LeaveApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveApplication
        fields = "__all__"


    def get_extra_kwargs(self,*args,**kwargs):
        extra_kwargs = super().get_extra_kwargs(*args,**kwargs)
        extra_kwargs['id'] = {'read_only' : True}
        extra_kwargs['user'] = {'read_only' : False}
        extra_kwargs['number_of_leave_days'] = {'read_only' : True}
        extra_kwargs['application_date'] = {'read_only' : True}

        if not self.context['request'].user.role == 'admin':
            extra_kwargs['application_date'] = {'read_only': True}
            extra_kwargs['user'] = {'read_only': True}
        return extra_kwargs

    def create(self, validated_data):
        return  LeaveApplication.objects.create(**validated_data)




