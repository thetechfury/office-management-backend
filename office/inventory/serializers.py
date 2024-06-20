from rest_framework import serializers
from .models import ItemCategory,Item

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
            'id':{'read_only':True}
        }
