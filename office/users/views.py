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
from .paginations import MyPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from inventory.models import Item,UserItemAssignment
from inventory.serializers import ItemSerializer,AssignedItemSerializer



class UserViewset(ModelViewSet):
    permission_classes = [IsAuthenticated,OnlyAdminUserCanMakePostRequest]
    http_method_names = ["get","post",'patch',"delete"]


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
        user_role = self.request.query_params.get('role')
        if self.request.user.role == 'admin':
            if user_role:
                return User.objects.filter(role = user_role)
            return User.objects.all()
        else:
            return User.objects.filter(id=user.id)


    def get_team_serialized_data(self,teams):
        if teams:
            return TeamListSerializerWithoutMembers(teams, many=True).data
        return []


    def get_assigned_items_serialized_data(self,assigned_items):
        if assigned_items:
            return AssignedItemSerializer(assigned_items, many=True).data
        return []


    def get_inventory_items_serialized_data(self,items):
        if items:
            return ItemSerializer(items, many=True).data
        return []


    def get_user_teams(self,user):
        teams = Team.objects.filter(members__user=user)
        return self.get_team_serialized_data(teams)


    def get_user_assigned_items(self,user):
        assigned_items= UserItemAssignment.objects.filter(user=user)
        return self.get_assigned_items_serialized_data(assigned_items)

    def get_all_assigned_items(self):
        all_assigned_items = UserItemAssignment.objects.all()
        return self.get_assigned_items_serialized_data(all_assigned_items)


    def get_all_teams(self):
        teams = Team.objects.all()
        return self.get_team_serialized_data(teams)


    def get_all_inventory_items(self):
        items = Item.objects.all()
        return self.get_inventory_items_serialized_data(items)

    def get_non_admin_response(self):
        user = User.objects.get(id=self.request.user.id)
        user_serializer = UserSerializer(user)
        response = {
            'user': user_serializer.data,
            'user_teams': self.get_user_teams(user),
            'user_items': self.get_user_assigned_items(user),
        }
        if self.request.user.role == "inventory_manager":
            response['all-items'] = self.get_all_inventory_items(),
            response['all_assigned_items'] = self.get_all_assigned_items(),
            return response
        else:
            return response


    def list(self, request, *args, **kwargs):
        if request.user.role == "admin":
            queryset = User.objects.exclude(email= request.user.email)
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
            current_user = User.objects.get(email = request.user.email)
            current_user_serilized_data = UserSerializer(current_user).data

            response = {
                'number_of_active_users': number_of_active_users,
                'total_users': total_users,
                'total_teams': total_teams,
                'user': current_user_serilized_data ,
                'all_users':serializer.data,
                'all_teams': self.get_all_teams(),
                'user_teams': self.get_user_teams(request.user),
                'inventory_items' : self.get_all_inventory_items(),
                'all_assigned_items':self.get_all_assigned_items(),
                'user_items': self.get_user_assigned_items(request.user)
            }
            return Response(response)
        else:
            return Response(self.get_non_admin_response())

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


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



    def get_queryset(self):
        user = self.request.user
        if user == "admin":
            return Profile.objects.all()

        profile = Profile.objects.filter(user = user)
        return profile


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








