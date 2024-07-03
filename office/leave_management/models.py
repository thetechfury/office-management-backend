import datetime
from django.db import models
from users.models import User
from rest_framework import serializers

# Create your models here.
CASUAL = 'casual'
ANNUAL = 'annual'
MEDICAL = 'medical'

Leave_type = (
    (CASUAL, "Casual"),
    (ANNUAL, "Annual"),
    (MEDICAL, "Medical")
)


class LeaveApplication(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    Leave_status = (
        (PENDING, "Pending"),
        (ACCEPTED, "Accepted"),
        (REJECTED, "Rejected")
    )

    application_date = models.DateField(auto_now=True)
    leave_type = models.CharField(max_length=8,default=MEDICAL,choices=Leave_type)
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_leave_days = models.PositiveIntegerField()
    reason = models.CharField(max_length=400)
    attachment = models.FileField(upload_to="application_file",null=True,blank=True)
    leave_status = models.CharField(max_length=10,choices=Leave_status,default=PENDING)
    user = models.ForeignKey(User,on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.user.email} - {self.leave_type} - {self.leave_status}"

    def save(self, *args, **kwargs):
        # Calculate the number of days between start_date and end_date
        self.number_of_leave_days = (self.end_date - self.start_date).days
        if self.number_of_leave_days < 1 or  not self.number_of_leave_days :
            raise serializers.ValidationError("end date must be greater than start_date")
        super().save(*args, **kwargs)



class UserLeaves(models.Model):
    leave_type = models.CharField(max_length=8,default=MEDICAL,choices=Leave_type)
    number_of_leaves = models.PositiveIntegerField()
    remaining_leaves = models.IntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.user.email} -{self.remaining_leaves}/{self.number_of_leaves}"

    def save(self, *args, **kwargs):
        # Calculate the number of days between start_date and end_date
        self.rem = (self.end_date - self.start_date).days
        if self.number_of_leave_days < 1 or  not self.number_of_leave_days :
            raise serializers.ValidationError("end date must be greater than start_date")
        super().save(*args, **kwargs)
