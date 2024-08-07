from django.contrib.auth import authenticate,logout

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.validators import ValidationError
from rest_framework.decorators import action
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import User, Team, Membership, Profile, ProfileImage, Skills, WorkingExperience, Education,Address
from .serializers import (
    UserSerializer, UpdatePasswordSerializer, TeamSerializer, AdminUserUpdateSerializer,
    UserPostSerializer, UserUpdateSerializer, MembershipSerializer, ProfileSerializer,
    ProfileImageSerializer, ProfileSkillSerializer, LoginSerializer, WorkingExperienceSerializer,
    AdminListUserSerializer, ProfileEducationSerializer, AddressSerializer,
    UserForForeignKeySerializer, TeamForForeignKeySerializer,LoginSerializer
)

from utils.permissions import OnlyAdminUserCanMakePostRequest, ProfilePermissions,OnlyAdminUser,OnlyAdminUserCanPostAndDelete
from utils.paginations import DefaultPagePagination,MyPagination

class UserViewset(ModelViewSet):
    permission_classes = [IsAuthenticated,OnlyAdminUserCanPostAndDelete]
    http_method_names = ["get","post",'patch',"delete"]
    pagination_class = DefaultPagePagination
    filterset_fields = ['email','role']
    serializer_class = UserSerializer

    # need to modify if end user make post request
    def get_serializer_class(self):
        if getattr(self, "swagger_fake_view", False):
            # queryset just for schema generation metadata
            return UserSerializer
        role = self.request.user.role
        action = self.action
        if role == "admin":
            if action == 'list':
                return AdminListUserSerializer
            elif action == 'create':
                return UserPostSerializer
            elif action in ['update', 'partial_update']:
                return AdminUserUpdateSerializer
        elif action in ['update', 'partial_update']:
            return UserUpdateSerializer

        return UserSerializer


    def get_queryset(self):
        user = self.request.user
        if self.request.user.role == 'admin':
            return User.objects.all()
        return User.objects.filter(id=user.id)


    @swagger_auto_schema(
        operation_id='API to get Users based on thier roles',
        operation_summary="View User detail",
    )
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

    @swagger_auto_schema(
        operation_id='API to create user',
        operation_summary="Only Admin User can create a user",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request,*args,**kwargs)


    @swagger_auto_schema(
        operation_id='API to get single user based on id',
        operation_summary="Single user data",

    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request,*args,**kwargs)



    @swagger_auto_schema(
        operation_id='Only Admin User can delete User',
        operation_summary="Remove User",
        operation_description='Display inside',
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)



class GetuserForForeignKey(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,*args):
            users = User.objects.all()
            serializer = UserForForeignKeySerializer(users,many=True)
            return Response(serializer.data)

class GetuserToChangeTeamLeader(APIView):
    permission_classes = [IsAuthenticated,OnlyAdminUser]

    def get(self,request,team_id,*args):
        try:
            team = Team.objects.get(id = team_id)
            members = team.members.exclude(user=team.leader)
            users = User.objects.filter(membership__in=members)
            serializer = UserForForeignKeySerializer(users,many=True)
            return Response(serializer.data)
        except:
            raise ValidationError("This id has no team")



class GetTeamAsForeignKey(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,*args):
            if request.user.role != "admin":
                teams = Team.objects.filter(leader = request.user)
                serializer = TeamForForeignKeySerializer(teams,many=True)
                return Response(serializer.data)
            else:
                teams = Team.objects.all()
                serializer = TeamForForeignKeySerializer(teams,many=True)
                return Response(serializer.data)

class GetUserProfile(APIView):
    def get(self,request,user_id):
        try:
            profile = Profile.objects.get(user_id = user_id)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except:
            return Response({'message':"This user has no Profile"})


class GetUserSkills(APIView):
    def get(self,request,user_id):
        try:
            profile = Profile.objects.get(user_id = user_id)
            skills = Skills.objects.filter(profile = profile)
            serializer = ProfileSkillSerializer(skills,many=True)
            return Response(serializer.data)
        except:
            return Response({'message':"This user has no Skills in Database"})


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

# Can be modified
class GetUserTeams(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,user_id):
            try:
                user = User.objects.get(id = user_id)
                user_teams = Team.objects.filter(members__user=user)
                number_of_teams = user_teams.count()
                user_team_serializer = TeamSerializer(user_teams, many=True)
                return Response({'user_teams': user_team_serializer.data, 'number_of_user_teams': number_of_teams})
            except:
                return Response({'message': "This Id has no user"})

            return Response({'message': 'This user has no Team'})


# This should be patch because if we put avail more payload  than patch and also put try to save instance if does't found
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
    authentication_classes = [TokenAuthentication,OnlyAdminUserCanMakePostRequest]
    permission_classes = [IsAuthenticated]
    pagination_class = MyPagination
    http_method_names = ["get",'post','patch','delete']

    def list(self, request, *args, **kwargs):
        if request.user.role != "admin":
            queryset = Team.objects.filter(leader=request.user)
            serializer = TeamSerializer(queryset,many=True)
            return Response(serializer.data)
        else:
            queryset = Team.objects.all()
            serializer = TeamSerializer(queryset, many=True)
            return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def list_teams_by_leader(self, request, *args, **kwargs):
        leader_id = request.query_params.get('leader_id')
        if not leader_id:
            return Response({"error": "Leader ID is required"}, status=400)

        teams = self.queryset.filter(leader_id=leader_id)
        serializer = self.get_serializer(teams, many=True)
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
            return []



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



class LoginAPI(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]
    http_method_names = ["post"]
    serializer_class = LoginSerializer

    @swagger_auto_schema(operation_description="To Login ",request_body=LoginSerializer)
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








