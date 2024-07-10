from django.contrib import admin
from .models import LeaveApplication,UserLeaves
# Register your models here.

admin.site.register(LeaveApplication)
admin.site.register(UserLeaves)
