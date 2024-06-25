from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import User, Team, Membership, Profile, Education, ProfileImage, Skills, WorkingExperience
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
        instance.bio = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        instance.save()
        return instance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email','role','full_name']
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
        user = super().update(instance, validated_data)
        user.save()
        return user


class AdminListUserSerializer(serializers.ModelSerializer):
     class Meta:
        model = User
        fields = ['full_name','email','role','date_joined','is_active','id']

     def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date_joined'] = instance.date_joined.strftime('%Y-%m-%d')
        return representation


class UpdatePasswordSerializer(serializers.Serializer):
    previous_password = serializers.CharField(max_length=50)
    new_password = serializers.CharField(max_length=50)
    confirm_password = serializers.CharField(max_length=50)




class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = "__all__"

    def create(self, validated_data):
        member = Membership.objects.create(**validated_data)
        return member

class TeamSerializer(serializers.ModelSerializer):
    members = MembershipSerializer(many=True, read_only=True)
    class Meta:
        model = Team
        fields = ['id','name','leader','members']
        extra_kwargs = {
            'id':{'read_only' : True}
        }

    def create(self, validated_data):
        team = Team.objects.create(**validated_data)
        leader = validated_data.pop('leader')
        Membership.objects.create(user = leader,team = team)
        return team


class EductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"
        extra_kwargs ={
            'id':{'read_only':True},
            'profile': {"write_only" : True}
        }
class ProfileSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = '__all__'
        read_only_fields = ('id','profile',)
        validators = [
            UniqueTogetherValidator(
                queryset=Skills.objects.all(),
                fields=['name']
            )
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        profile = Profile.objects.get(user=user)
        profile_skill = Skills.objects.create(**validated_data,profile = profile)
        return profile_skill

    def update(self, instance, validated_data):
            instance.name = validated_data.get('name')
            instance.level = validated_data.get('level')
            instance.description = validated_data.get('description')
            instance.save()
            return instance


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = '__all__'
        read_only_fields = ('id', 'profile',)

    def validate(self, data):
        user = self.context['request'].user
        try:
            profile = Profile.objects.get(user=user)
            if ProfileImage.objects.filter(profile=profile).exists() and self.context['view'].action != 'update':
                raise serializers.ValidationError("A profile image already exists for this user.")
            return data
        except:
            raise serializers.ValidationError(f"No Profile created against {user.email} user ")

    def create(self, validated_data):
        user = self.context['request'].user
        profile = Profile.objects.get(user=user)
        profile_image = ProfileImage.objects.create(**validated_data, profile=profile)
        return profile_image

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title')
        instance.save()
        return instance


class WorkingExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingExperience
        fields = '__all__'
        read_only_fields = ('id','profile',)
        validators = [
            UniqueTogetherValidator(
                queryset=WorkingExperience.objects.all(),
                fields=['title','company_name','joining_date']
            )
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        profile = Profile.objects.get(user=user)
        working_experience = WorkingExperience.objects.create(**validated_data,profile = profile)
        return working_experience

    def update(self, instance, validated_data):
            instance.title = validated_data.get('title')
            instance.company_name = validated_data.get('company_name')
            instance.description = validated_data.get('description')
            instance.joining_date = validated_data.get('joining_date')
            instance.end_date = validated_data.get('end_date')
            instance.remarks = validated_data.get('remarks')
            instance.save()
            return instance



class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    educations =  EductionSerializer(many = True,read_only=True)
    profile_image = ProfileImageSerializer(read_only = True)
    skills = ProfileSkillSerializer(many = True,read_only = True)
    experience = WorkingExperienceSerializer(many = True,read_only = True)
    class Meta:
        model = Profile
        fields = ['id','date_of_birth','bio','phone','user','educations','profile_image','skills','experience']
        read_only_fields = ('id','user')


    def validate(self, data):
        user = self.context['request'].user
        if Profile.objects.filter(user=user).exists() and self.context['view'].action != 'update':
            raise serializers.ValidationError("A profile already exists for this user.")
        return data



    def create(self, validated_data):
        user = self.context['request'].user
        profile = Profile.objects.create(**validated_data,user = user)
        return profile


    def update(self, instance, validated_data):
            instance.bio = validated_data.get('bio', instance.bio)
            instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
            instance.save()
            return instance







class ProfileEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'
        read_only_fields = ('id', 'profile',)


        validators = [
            UniqueTogetherValidator(
                queryset=Education.objects.all(),
                fields=['degree']
            )
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            profile = Profile.objects.get(user=user)
        except:
            serializers.ValidationError("To add Education User must has profile")
        profile_education = Education.objects.create(**validated_data,profile = profile)
        return profile_education

    def update(self, instance, validated_data):
            instance.degree = validated_data.get('degree')
            instance.total_marks = validated_data.get('total_marks')
            instance.obtain_marks = validated_data.get('obtain_marks')
            instance.start_date = validated_data.get('start_date')
            instance.end_date = validated_data.get('end_date')
            instance.institute = validated_data.get('institute')
            instance.save()
            return instance




class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)
