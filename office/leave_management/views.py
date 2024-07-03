from rest_framework import viewsets
from .models import LeaveApplication
from .serializers import LeaveApplicationSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class LeaveApplicationViewset(viewsets.ModelViewSet):
    serializer_class = LeaveApplicationSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated,]
    http_method_names = ("get", "post", "patch", "delete")

    def get_queryset(self):
        if self.request.user.role != "admin":
            return LeaveApplication.objects.filter(user = self.request.user)

        return LeaveApplication.objects.all().order_by('-application_date')



class LeavesViewset(viewsets.ModelViewSet):
    pass