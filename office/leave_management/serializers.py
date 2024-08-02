from rest_framework import serializers
from .models import LeaveApplication,UserLeaves
class LeaveApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveApplication
        fields = "__all__"


    # def get_extra_kwargs(self,*args,**kwargs):
    #     extra_kwargs = super().get_extra_kwargs(*args,**kwargs)
    #     if getattr(self, 'swagger_fake_view', False):
    #         return extra_kwargs
    #
    #     extra_kwargs['id'] = {'read_only' : True}
    #     extra_kwargs['number_of_leave_days'] = {'read_only' : True}
    #     extra_kwargs['application_date'] = {'read_only' : True}
    #     extra_kwargs['rejoining_date'] = {'read_only': True}
    #     extra_kwargs['leave_status'] = {'read_only': True}
    #     extra_kwargs['user'] = {'read_only': True}
    #     extra_kwargs['is_cancel'] = {'read_only': True}
    #
    #     if self.context['request'].user.role == 'admin':
    #         extra_kwargs['leave_status'] = {'read_only': False}
    #         extra_kwargs['user'] = {'read_only': False}
    #
    #     return extra_kwargs

    # def create(self, validated_data):
    #     return  LeaveApplication.objects.create(**validated_data)


class UserLeavesSerializer(serializers.ModelSerializer):
        model = UserLeaves
        fields = "__all__"
        extra_kwargs = {
            'id' : {'read_only' : True},
            'remaining_leaves' : {'read_only' : True}
        }


        def create(self, validated_data):
            return UserLeaves.objects.create(**validated_data)

