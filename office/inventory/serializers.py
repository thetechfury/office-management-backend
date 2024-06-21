from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import ItemCategory,Item,StockMovement,UserItemAssignment

class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True}
        }


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"
        extra_kwargs ={
            'id':{'read_only':True},
            'remaining_quantity':{'read_only':True},
        }

    def create(self, validated_data):
        quantity = validated_data.get('total_quantity')
        return Item.objects.create(**validated_data,remaining_quantity = quantity)



class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = '__all__'

    def check_item_assigned_to_user(self,item,user):
        try:
            assigned_item = UserItemAssignment.objects.get(item = item,user = user)
            return assigned_item
        except:
            return False

    def change_item_quantity(self,item,quantity,movemnt_type):
        if movemnt_type == 'in':
            item.remaining_quantity += quantity
            item.save()
        else:
            item.remaining_quantity -= quantity
            item.save()

    def update_item_assignment_quantity(self,item,change_quantity):
        item.quantity -= change_quantity
        item.save()
        return item.quantity

    def validate(self, data):
        # we can't in or out if quantity we passed greater than item quantity
        if data['item'].remaining_quantity< data['quantity_change'] and data['movement_type'] == 'out':
            if data['item'].remaining_quantity == 0:
                raise ValidationError("This  item is not availabe in stock")
            raise ValidationError("The Demand quantity is not available in stock ")

        if data['quantity_change'] < 1:
            raise ValidationError("Change value must be greater than zero")

        return data

    def create(self, validated_data):
        movement_type = validated_data.get('movement_type')
        quantity_change = validated_data.get('quantity_change')
        item = validated_data.get('item')
        user = validated_data.get('user')
        if movement_type == 'out' and quantity_change <= item.remaining_quantity:
            item_already_assigned = self.check_item_assigned_to_user(item, user)
            if not item_already_assigned:
                UserItemAssignment.objects.create(user = user,item = item,quantity = quantity_change)
            self.change_item_quantity(item,quantity_change,movement_type)


        elif  movement_type == 'in':
            item_already_assigned = self.check_item_assigned_to_user(item,user)
            if not item_already_assigned:
                raise ValidationError("You can't in item because user has no such item")
            else:
                if quantity_change <= item_already_assigned.quantity:
                    self.change_item_quantity(item, quantity_change, movement_type)
                    assignment_quantaty = self.update_item_assignment_quantity(item_already_assigned,quantity_change)
                    if not assignment_quantaty:
                        item_already_assigned.delete()
                else:
                    raise ValidationError("This user has less quantity than you requested")
        return  StockMovement.objects.create(**validated_data)




class UserItemAssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserItemAssignment
        fields = '__all__'




class ItemPartialUpdateSerializer(serializers.ModelSerializer):
    additional_quantity = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Item
        fields = ['additional_quantity']

    def update(self, instance, validated_data):
        additional_quantity = validated_data.get('additional_quantity', 0)
        instance.total_quantity += additional_quantity
        instance.remaining_quantity += additional_quantity
        instance.save()
        return instance