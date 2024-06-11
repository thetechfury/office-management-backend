from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rest_framework.viewsets import ModelViewSet
from .models import User, Team, Membership
from .serializers import UserSerializer, UpdatePasswordSerializer, TeamSerializer, AdminUserUpdateSerializer, \
    AdminUserPostSerializer, UserUpdateSerializer,MembershipSerializer
from .permissions import MyPermission, TeamPermission, MembershipPermission
from rest_framework.validators import ValidationError
from rest_framework.pagination import PageNumberPagination
from .paginations import MyPagination

class UserViewset(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication,BasicAuthentication]
    permission_classes = [IsAuthenticated,MyPermission]
    pagination_class = MyPagination

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



class UpdatePasswordAPI(UpdateAPIView):
    serializer_class = UpdatePasswordSerializer
    permission_classes = [IsAuthenticated]

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

    def get_queryset(self):
        user = self.request.user
        if self.request.user.role == 'admin':
            return Team.objects.all()
        else:

            return Team.objects.filter(leader=user)



class MembershipViewset(ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated,MembershipPermission]
    pagination_class = MyPagination


    def get_queryset(self):
        teams= Team.objects.filter(leader = self.request.user)
        if teams:
            members = Membership.objects.filter(team_id__in = teams).order_by('team')
            return members
        else:
            return ValidationError("This user is not leader of any team")
















