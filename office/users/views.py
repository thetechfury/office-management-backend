from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import authenticate,logout,login
from .models import User, Team, Membership, Profile, ProfileImage, Skills, WorkingExperience, Education,Address
from .serializers import UserSerializer, UpdatePasswordSerializer, TeamSerializer, AdminUserUpdateSerializer, \
    AdminUserPostSerializer, UserUpdateSerializer, MembershipSerializer, ProfileSerializer, ProfileImageSerializer, \
    ProfileSkillSerializer, LoginSerializer, WorkingExperienceSerializer, AdminListUserSerializer, \
    ProfileEducationSerializer, AddressSerializer, TeamListSerializerWithoutMembers
from utils.permissions import OnlyAdminUserCanMakePostRequest, TeamPermission, ProfilePermissions
from rest_framework.validators import ValidationError
from utils.paginations import DefaultPagePagination,MyPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from inventory.models import Item,UserItemAssignment
from inventory.serializers import ItemSerializer,AssignedItemSerializer


class UserViewset(ModelViewSet):
    permission_classes = [IsAuthenticated,OnlyAdminUserCanMakePostRequest]
    http_method_names = ["get","post",'patch',"delete"]
    queryset = User.objects.all()
    pagination_class = DefaultPagePagination
    filterset_fields = ['email','role']




    def get_serializer_class(self):
        role = self.request.user.role
        action = self.action
        if role == "admin":
            if action == 'list':
                return AdminListUserSerializer
            elif action == 'create':
                return AdminUserPostSerializer
            elif action in ['update', 'partial_update']:
                return AdminUserUpdateSerializer
        elif action in ['update', 'partial_update']:
            return UserUpdateSerializer

        return UserSerializer


    def get_queryset(self):
        user = self.request.user
        if self.request.user.role == 'admin':
            return User.objects.exclude(email = self.request.user.email)
        else:
            return User.objects.filter(id=user.id)


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # convert queryset in paginated queryset
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            if request.user.role == 'admin':
                total_users = queryset.count()
                number_of_active_user = User.objects.filter(is_active = True).count()
                current_user = User.objects.get(email = request.user.email)
                paginated_response.data['user'] = UserSerializer(current_user).data
                paginated_response.data['total_users'] = total_users
                paginated_response.data['number_of_active_users'] = number_of_active_user

            return paginated_response

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class GetUserProfile(APIView):
    def get(self,request,user_id):
        try:
            profile = Profile.objects.get(user_id = user_id)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except:
            return Response({'message':"This user has no Profile"})

class GetUserAddress(APIView):
    def get(self,request,user_id):
        try:
            profile = Profile.objects.get(user_id = user_id)
            address = Address.objects.get(profile = profile)
            serializer = AddressSerializer(address)
            return Response(serializer.data)
        except:
            return Response({'message':"This user has no Address"})

class GetUserExperience(APIView):
    def get(self,request,user_id):
            profile = Profile.objects.get(user_id = user_id)
            experience = WorkingExperience.objects.filter(profile = profile)
            serializer = WorkingExperienceSerializer(experience,many=True)
            return Response(serializer.data)


class GetUserEducation(APIView):
    def get(self,request,user_id):
            profile = Profile.objects.get(user_id = user_id)
            education = Education.objects.filter(profile = profile)
            serializer = ProfileEducationSerializer(education,many=True)
            return Response(serializer.data)


class UpdatePasswordAPI(UpdateAPIView):
    serializer_class = UpdatePasswordSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["put"]

    def update(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            previous_password = serializer.data.get('previous_password')
            new_password = serializer.data.get('new_password')
            confirm_password = serializer.data.get('confirm_password')
            if not user.check_password(previous_password):
                return Response({"response":" wrong password"})
            if new_password != confirm_password:
                return Response({"response": "new password and confirm password does't match"})
            user.set_password(confirm_password)
            user.save()
            return Response({"response":"Password changed"},status=status.HTTP_200_OK)
        else:
            Response(serializer.errors)



class TeamViewset(ModelViewSet):
    queryset = Team.objects.all()
    serializer_class =TeamSerializer
    permission_classes = [IsAuthenticated,TeamPermission]
    pagination_class = MyPagination
    http_method_names = ["get",'post','patch','delete']

    def list(self, request, *args, **kwargs):
        if request.user.role == "admin":
            queryset = Team.objects.all()
        else:
            queryset = Team.objects.filter(leader=request.user)
        queryset = Team.objects.filter(leader=request.user)
        serializer = TeamSerializer(queryset,many=True)

        return Response(serializer.data)



class MembershipViewset(ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get",'post','delete']

    def get_queryset(self):
        # admin user can access all members of all teams
        if self.request.user.role == 'admin':
            return Membership.objects.all()
        # if team leader request
        teams= Team.objects.filter(leader = self.request.user)
        if teams:
            members = Membership.objects.filter(team_id__in = teams)
            return members
        # if member is not team leader but part of teams

        else:
            return ValidationError("This user is not belongs  of any team")



class ProfileViewset(ModelViewSet):
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,ProfilePermissions]
    http_method_names = ["get",'post','delete','patch']
    pagination_class = DefaultPagePagination




    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Profile.objects.all().exclude(user = user)

        profile = Profile.objects.filter(user = user)
        return profile

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # convert queryset in paginated queryset
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            if request.user.role == 'admin':
                admin_user_profile = Profile.objects.get(user = request.user)
                paginated_response.data['user_profile'] = ProfileSerializer(admin_user_profile).data

            return paginated_response

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProfileImageViewset(ModelViewSet):
    queryset = ProfileImage.objects.all()
    serializer_class = ProfileImageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ("get","post","put")
    def get_queryset(self):
        try:
            profile = Profile.objects.get(user=self.request.user)
            profile_image = ProfileImage.objects.filter(profile=profile)
            return profile_image
        except:
            return []

class ProfileEducationViewset(ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = ProfileEducationSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ("get","post","put")
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            # Return an empty queryset or a queryset with dummy data to avoid issues during schema generation
            return Profile.objects.none()

        user = self.request.user
        if user.role == "admin":
            profile_education = Education.objects.all()
            return profile_education
        else:
            profile = Profile.objects.filter(user = user)
            return  Education.objects.filter(profile = profile)



class ProfileAddressViewset(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ("get","post","put")
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            # Return an empty queryset or a queryset with dummy data to avoid issues during schema generation
            return Address.objects.none()

        user = self.request.user
        if user.role == "admin":
            profile_address = Address.objects.all()
            return profile_address
        else:
            profile = Profile.objects.filter(user = user)
            return  Address.objects.filter(profile = profile)

class ProfileSkillViewset(ModelViewSet):
    queryset = Skills.objects.all()
    serializer_class = ProfileSkillSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ("get","post","patch")
    def get_queryset(self):
        user = self.request.user
        try:
            profile = Profile.objects.get(user=self.request.user)
            profile_skills = Skills.objects.filter(profile=profile)
            return profile_skills
        except:
            return []

class WorkingExperienceViewset(ModelViewSet):
    queryset = WorkingExperience.objects.all()
    serializer_class = WorkingExperienceSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ("get","post","patch","delete")
    def get_queryset(self):
        user = self.request.user
        try:
            profile = Profile.objects.get(user=self.request.user)
            working_experience = WorkingExperience.objects.filter(profile=profile)
            return working_experience
        except:
            return []


class GetWorkExperience(APIView):
    pass

class LoginAPI(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]
    http_method_names = ["post"]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = authenticate(username=email, password=password)
            if not user:
                raise ValidationError("Incorrect username or password.")

            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})



class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            logout(request)
            return Response({"message":"You Logged out"})
        except:
            raise ValidationError("Error occur while logging out")








