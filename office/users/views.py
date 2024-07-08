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
    ProfileEducationSerializer,AddressSerializer
from .permissions import MyPermission, TeamPermission, ProfilePermissions
from rest_framework.validators import ValidationError
from .paginations import MyPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token



class UserViewset(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,MyPermission]
    # pagination_class = MyPagination
    http_method_names = ["get","post",'patch',"delete"]
    filter_backends = [filters.SearchFilter]
    # filterset_fields = ['is_active']
    search_fields = ['users__role']


    def get_serializer_class(self):
        if self.request.user.role == "admin" and self.action == 'list':
            return AdminListUserSerializer
        elif self.request.user.role == "admin" and self.action == 'create':
            return AdminUserPostSerializer
        elif self.request.user.role == "admin" and self.action in ['update','partial_update']:
            return AdminUserUpdateSerializer
        elif self.request.user.role != "admin" and self.action in ['update','partial_update'] :
            return UserUpdateSerializer
        return UserSerializer


    def get_queryset(self):
        user = self.request.user
        user_role = self.request.query_params.get('role')
        if self.request.user.role == 'admin':
            if user_role:
                return User.objects.filter(role = user_role)
            return User.objects.all()
        else:
            return User.objects.filter(id=user.id)

    def list(self, request, *args, **kwargs):
        if request.user.role == "admin":
            queryset = User.objects.all()
            user_role = self.request.query_params.get('role')
            user_active = self.request.query_params.get('active')
            if user_role and user_active:
                queryset = User.objects.filter(role=user_role,is_active = user_active)
            elif user_role:
                queryset = User.objects.filter(role=user_role)
            elif user_active:
                queryset = User.objects.filter(is_active=user_active)

            serializer = AdminListUserSerializer(queryset,many=True)
            number_of_active_users = User.objects.filter(is_active = True).count()
            total_users = User.objects.count()
            total_teams = Team.objects.count()
            active_user_percentage = self.get_active_user_percentage(total_users,number_of_active_users)
            response = {
                'number_of_active_users': number_of_active_users,
                'total_users': total_users,
                'total_teams': total_teams,
                'active_user_percentage':active_user_percentage,
                'users':serializer.data,


            }
            return Response(response)
        else:
            queryset = User.objects.get(id = request.user.id)
            serializer = UserSerializer(queryset)


            return Response(serializer.data)

    def get_active_user_percentage(self,total_user,active_user):
        active_user_percentage = (active_user/total_user) * 100
        return active_user_percentage







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

class ProfileEducationViewset(ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = ProfileEducationSerializer
    authentication_classes = [BasicAuthentication]
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
    authentication_classes = [BasicAuthentication]
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








