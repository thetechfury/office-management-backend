from rest_framework import serializers
from .models import LeaveApplication,UserLeaves
class LeaveApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveApplication
        fields = "__all__"


    def get_extra_kwargs(self,*args,**kwargs):
        extra_kwargs = super().get_extra_kwargs(*args,**kwargs)
        extra_kwargs['id'] = {'read_only' : True}
        extra_kwargs['number_of_leave_days'] = {'read_only' : True}
        extra_kwargs['application_date'] = {'read_only' : True}
        extra_kwargs['rejoining_date'] = {'read_only': True}
        extra_kwargs['leave_status'] = {'read_only': True}
        extra_kwargs['user'] = {'read_only': True}
        extra_kwargs['is_cancel'] = {'read_only': True}

        if self.context['request'].user.role == 'admin':
            extra_kwargs['leave_status'] = {'read_only': False}
            extra_kwargs['user'] = {'read_only': False}


        return extra_kwargs

    # def create(self, validated_data):
    #     return  LeaveApplication.objects.create(**validated_data)


class LeavesSerializer(serializers.ModelSerializer):
    # PENDING = 'pending'
    # ACCEPTED = 'accepted'
    # REJECTED = 'rejected'
    #
    # Leave_status = (
    #     (PENDING, "Pending"),
    #     (ACCEPTED, "Accepted"),
    #     (REJECTED, "Rejected")
    # )
    #
    # application_date = models.DateField(auto_now=True)
    # leave_type = models.CharField(max_length=8,default=MEDICAL,choices=Leave_type)
    # start_date = models.DateField()
    # end_date = models.DateField()
    # rejoining_date = models.DateField()
    # number_of_leave_days = models.PositiveIntegerField()
    # reason = models.CharField(max_length=400)
    # attachment = models.FileField(upload_to="application_file",null=True,blank=True)
    # leave_status = models.CharField(max_length=10,choices=Leave_status,default=PENDING)
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    # is_cancel = models.BooleanField(default=False)
    class Meta:
        model = UserLeaves
        fields = "__all__"

        def get_extra_kwargs(self, *args, **kwargs):
            extra_kwargs = super().get_extra_kwargs(*args, **kwargs)
            extra_kwargs['id'] = {'read_only': True}
            extra_kwargs['application_date'] = {'read_only': True}
            extra_kwargs['number_of_leave_days'] = {'read_only': True}
            extra_kwargs['rejoining_date'] = {'read_only': True}
            extra_kwargs['leave_status'] = {'read_only': True}
            extra_kwargs['user'] = {'read_only': True}
            extra_kwargs['is_cancel'] = {'read_only': True}



            return extra_kwargs

        def create(self, validated_data):
            return UserLeaves.objects.create(**validated_data)

