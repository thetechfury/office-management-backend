from django.contrib import admin
from .models import UserItemAssignment,StockMovement,Item
# Register your models here.
admin.site.register(UserItemAssignment)
admin.site.register(StockMovement)
admin.site.register(Item)