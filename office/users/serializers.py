from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import User, Team, Membership, Profile, Education, ProfileImage, Skills, WorkingExperience,Address
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



class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = "__all__"

    def create(self, validated_data):
        member = Membership.objects.create(**validated_data)
        return member

class TeamListSerializerWithoutMembers(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self.context.get('remove_profile'):
            representation.pop('profile')
        return representation


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



class UserSerializerForProfile(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'role', 'date_joined', 'is_active', 'id','date_joined']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date_joined'] = instance.date_joined.strftime('%d %b %Y')
        return representation




class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image')

    def get_image(self, obj):
        try:
            image = Profile.objects.get(user=obj).profile_image.image
            return image.path
        except:
            return False

    class Meta:
        model = User
        fields = ['id', 'email','role','full_name','image','profile','date_joined']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_superuser': {'read_only': True},
            'is_staff': {'read_only': True},
            'role': {'read_only': True}
        }


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date_joined'] = instance.date_joined.strftime('%d %b %Y')
        if self.context.get('remove_both_image_and_profile'):
            representation.pop('image')
            representation.pop('profile')
        return representation

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        user.save()
        return user


class EductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"
        extra_kwargs ={
            'id':{'read_only':True},
            'profile': {"write_only" : True}
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['start_date'] = instance.start_date.strftime('%d %b %Y')
        representation['end_date'] = instance.end_date.strftime('%d %b %Y')
        return representation




class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = '__all__'
        read_only_fields = ('id', 'profile',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self.context.get('remove_profile', False):
            representation.pop('profile', None)
        return representation

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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['joining_date'] = instance.joining_date.strftime('%d %b %Y')
        representation['end_date'] = instance.end_date.strftime('%d %b %Y')
        if self.context.get('remove_profile', False):
            representation.pop('profile', None)
        return representation

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


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ('id','profile',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self.context.get('remove_profile', False):
            representation.pop('profile', None)
        return representation


    def create(self, validated_data):
        user = self.context['request'].user
        profile = Profile.objects.get(user=user)
        address = Address.objects.create(**validated_data,profile = profile)
        return address

    def update(self, instance, validated_data):
            instance.city = validated_data.get('city')
            instance.state = validated_data.get('state')
            instance.street = validated_data.get('street')
            instance.country = validated_data.get('country')
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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['start_date'] = instance.start_date.strftime('%d %b %Y')
        representation['end_date'] = instance.end_date.strftime('%d %b %Y')
        return representation



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





class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_user_without_image_and_profile')
    educations =  EductionSerializer(many = True,read_only=True)
    profile_image =serializers.SerializerMethodField()
    skills = serializers.SerializerMethodField('get_skills_without_profile_id')
    experience = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ['id','date_of_birth','bio','phone','user','educations','profile_image','skills','experience','address']
        read_only_fields = ('id','user')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date_of_birth'] = instance.date_of_birth.strftime('%d %b %Y')
        return representation

    def get_profile_image(self, obj):
        context = self.context.copy()
        context['remove_profile'] = True
        return ProfileImageSerializer(obj.profile_image, context=context).data

    def get_skills_without_profile_id(self,obj):
        context = self.context.copy()
        context['remove_profile'] = True
        return ProfileSkillSerializer(obj.skills, many=True, context=context).data

    def get_experience(self,obj):
        context = self.context.copy()
        context['remove_profile'] = True
        return WorkingExperienceSerializer(obj.experience, many=True, context=context).data

    def get_address(self,obj):
        context = self.context.copy()
        context['remove_profile'] = True
        return AddressSerializer(obj.address,read_only=True, context=context).data

    def get_user_without_image_and_profile(self,obj):
        context = self.context.copy()
        context['remove_both_image_and_profile'] = True
        return UserSerializer(obj.user,context=context).data





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





class AdminListUserSerializer(serializers.ModelSerializer):
     image = serializers.SerializerMethodField('get_image')

     def get_image(self, obj):
         try:
            image = Profile.objects.get(user = obj).profile_image.image
            return image.path
         except:
            return None
     class Meta:
        model = User
        fields = ['full_name','email','role','date_joined','is_active','id','image','profile']

     def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date_joined'] = instance.date_joined.strftime('%d %b %Y')
        return representation




class UpdatePasswordSerializer(serializers.Serializer):
    previous_password = serializers.CharField(max_length=50)
    new_password = serializers.CharField(max_length=50)
    confirm_password = serializers.CharField(max_length=50)








class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)

