from django.contrib import admin
from .models import Shift,Break,UserShift,Attendence
# Register your models here.

admin.site.register(Shift)
admin.site.register(Break)
admin.site.register(UserShift)
admin.site.register(Attendence)