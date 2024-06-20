from django.db import models
from users.models import User
# Create your models here.

class ItemCategory(models.Model):
    # CATEGORY_CHOICES = (
    #     ('office_essentials','Office Essentials'),
    #     ('electronics','Electronics'),
    #     ('furniture','Furniture'),
    # )

    name = models.CharField(max_length=30,unique=True)
    def __str__(self):
        return self.get_name_display()



class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300,null=True,blank=True)
    quantaty = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    category = models.ForeignKey(ItemCategory,on_delete=models.CASCADE)
    location = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.name



class StockMovement(models.Model):
    MOVEMENT_TYPE_CHOICES = (
        ('IN', 'in'),
        ('OUT', 'out'),
    )

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='stock_movements')
    quantity_change = models.IntegerField()
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    note = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.get_movement_type_display()} {self.quantity_change} of {self.item.name}"

class UserItemAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    remarks = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.item.name} assigned to {self.user.username}"

