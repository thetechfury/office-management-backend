from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import User,Team,Membership
from rest_framework.validators import ValidationError



class AdminUserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ( 'email','role','first_name','last_name','password')

        extra_kwargs = {
            'password': {'write_only': True},
            'is_superuser': {'read_only': True},
            'is_staff': {'read_only': True},
            'role': {'default': User.ENDUSER},
        }
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class AdminUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'role', 'first_name', 'last_name']
        extra_kwargs = {
            'is_superuser': {'read_only': True},
            'is_staff': {'read_only': True},
            'role': {'read_only': False}
        }

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        user.save()
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [  'first_name', 'last_name']
        extra_kwargs = {
            'is_superuser': {'read_only': True},
            'is_staff': {'read_only': True},
        }

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)

        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email','role','first_name','last_name']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_superuser': {'read_only': True},
            'is_staff': {'read_only': True},
            'role': {'read_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    def update(self, instance, validated_data):
        # password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        # if password:
        user.save()
        return user





class UpdatePasswordSerializer(serializers.Serializer):
    previous_password = serializers.CharField(max_length=50)
    new_password = serializers.CharField(max_length=50)
    confirm_password = serializers.CharField(max_length=50)


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"

    def create(self, validated_data):
        team = Team.objects.create(**validated_data)
        leader = validated_data.pop('leader')
        Membership.objects.create(user = leader,team = team)
        return team

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = "__all__"

    def create(self, validated_data):
        member = Membership.objects.create(**validated_data)
        return member