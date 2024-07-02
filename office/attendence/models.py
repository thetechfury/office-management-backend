from django.db import models
from users.models import User
from datetime import datetime
from datetime import timedelta

# Create your models here.
class Shift(models.Model):
    SHIFT_NAME_CHOICES = [
        ('Morning', 'Morning Shift'),
        ('Night', 'Night Shift'),
    ]

    name = models.CharField(max_length=20, choices=SHIFT_NAME_CHOICES, default='Custom')
    description = models.TextField(null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.name} ({self.start_time} - {self.end_time})"

class Break(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='breaks')
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration = models.DurationField()

    def save(self,*args,**kwargs):
        start_datetime = datetime.combine(datetime.min, self.start_time)
        end_datetime = datetime.combine(datetime.min, self.end_time)
        if end_datetime < start_datetime:
            end_datetime += timedelta(days=1)

        self.duration = end_datetime - start_datetime
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Break: {self.start_time} - {self.end_time} ({self.duration})"

class UserShift(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.user.email} - {self.shift.name} on {self.date}"


class Attendence(models.Model):
    CLOCK_IN = 'clock_in'
    CLOCK_OUT = 'clock_out'
    OPERTAION_CHOICES = (
        (CLOCK_IN,"Clock In"),
        (CLOCK_OUT,"Clock Out")
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    date = models.DateTimeField(auto_now=True)
    operation  = models.CharField(choices=OPERTAION_CHOICES,default=CLOCK_IN,max_length=10)

    def get_user_shift(self):
        try:
            return UserShift.objects.get(user=self.user)
        except UserShift.DoesNotExist:
            return None

    def __str__(self):
        return f"{self.user.email} {self.operation}"



