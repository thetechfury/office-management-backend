from rest_framework import viewsets
from .models import LeaveApplication, UserLeaves
from .serializers import LeaveApplicationSerializer,UserLeavesSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
# Create your views here.


class LeaveApplicationViewset(viewsets.ModelViewSet):
    serializer_class = LeaveApplicationSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ("get", "post", "patch", "delete")

    def get_queryset(self):
        if self.request.user.role != "admin":
            return LeaveApplication.objects.filter(user = self.request.user)

        return LeaveApplication.objects.all().order_by('-application_date')



class UserLeavesViewset(viewsets.ModelViewSet):
    serializer_class = UserLeavesSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ("get", "post", "patch", "delete")

    def get_queryset(self):
        if self.request.user.role != "admin":
            return UserLeaves.objects.filter(user = self.request.user)
        return UserLeaves.objects.all()