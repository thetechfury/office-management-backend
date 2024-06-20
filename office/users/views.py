from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import authenticate,logout,login
from django.http.response import JsonResponse
from django.db.models import OuterRef,Count
from .models import User, Team, Membership, Profile, ProfileImage, Skills, WorkingExperience
from .serializers import UserSerializer, UpdatePasswordSerializer, TeamSerializer, AdminUserUpdateSerializer, \
    AdminUserPostSerializer, UserUpdateSerializer, MembershipSerializer, ProfileSerializer, ProfileImageSerializer, \
    ProfileSkillSerializer, LoginSerializer,WorkingExperienceSerializer,AdminListUserSerializer
from .permissions import MyPermission, TeamPermission, MembershipPermission, ProfilePermissions
from rest_framework.validators import ValidationError
from rest_framework.pagination import PageNumberPagination
from .paginations import MyPagination

class UserViewset(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication,BasicAuthentication]
    permission_classes = [IsAuthenticated,MyPermission]
    pagination_class = MyPagination
    http_method_names = ["get","post",'patch',"delete"]


    def get_serializer_class(self):
        if self.request.user.role == "admin" and self.action == 'create':
            return AdminUserPostSerializer
        elif self.request.user.role == "admin" and self.action in ['update','partial_update']:
            return AdminUserUpdateSerializer
        elif self.request.user.role != "admin" and self.action in ['update','partial_update'] :
            return UserUpdateSerializer
        return UserSerializer


    def get_queryset(self):
        user = self.request.user
        if self.request.user.role == 'admin':
            return User.objects.all()
        else:
            return User.objects.filter(id=user.id)

    # def list(self, request, *args, **kwargs):
    #     my_teams = Team.objects.filter(membership__user=request.user)
    #     if request.user.role == "admin":
    #         queryset = User.objects.all()
    #         serializer = AdminListUserSerializer(queryset,many=True)
    #         total_users = User.objects.filter(is_active = True).count()
    #         total_teams = Team.objects.count()
    #         response = {
    #             'total_user': total_users,
    #             'total_teams': total_teams,
    #
    #             'users':serializer.data,
    #
    #         }
    #         return Response(response)
    #     else:
    #         queryset = User.objects.get(id = request.user.id)
    #         serializer = UserSerializer(queryset)
    #
    #
    #         return Response(serializer.data)







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
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated,TeamPermission]
    pagination_class = MyPagination
    http_method_names = ["get",'post','patch','delete']

    def list(self, request, *args, **kwargs):
        # if request.user.role == "admin":
        #     queryset = Team.objects.all()
        # else:
        #     queryset = Team.objects.filter(leader=request.user)
        queryset = Team.objects.filter(leader=request.user)
        serializer = TeamSerializer(queryset,many=True)

        return Response(serializer.data)



class MembershipViewset(ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = MyPagination
    http_method_names = ["get",'post','delete']




    def get_queryset(self):
        teams= Team.objects.filter(leader = self.request.user)
        if teams:
            members = Membership.objects.filter(team_id__in = teams).order_by('team')
            return members
        else:
            return ValidationError("This user is not leader of any team")



class ProfileViewset(ModelViewSet):
    serializer_class = ProfileSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated,ProfilePermissions]
    http_method_names = ["get",'post','delete','patch']

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            profiles = Profile.objects.all()
            return profiles
        else:
            profile = Profile.objects.filter(user = user)
            return profile


class ProfileImageViewset(ModelViewSet):
    queryset = ProfileImage.objects.all()
    serializer_class = ProfileImageSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ("get","post","put")
    def get_queryset(self):
        user = self.request.user
        try:
            profile = Profile.objects.get(user=self.request.user)
            profile_image = ProfileImage.objects.filter(profile=profile)
            return profile_image
        except:
            return []



class ProfileSkillViewset(ModelViewSet):
    queryset = Skills.objects.all()
    serializer_class = ProfileSkillSerializer
    authentication_classes = [BasicAuthentication]
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
    authentication_classes = [BasicAuthentication]
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
    authentication_classes = []
    http_method_names = ["post"]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = authenticate(username=email, password=password)
            if not user:
                raise ValidationError("Incorrect username or password.")
            else:
                login(request, user)
                return Response({"response": "You are successfully logged in."})
        else:
            return Response(serializer.errors, status=400)


class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            logout(request)
            return Response({"message":"You Logged out"})
        except:
            raise ValidationError("Error occur while logging out")








