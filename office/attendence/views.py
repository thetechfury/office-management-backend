from rest_framework import viewsets
from .models import Shift,Break,UserShift,Attendence
from .serializers import BreakSerializer,UserShiftSerializer,ShiftSerializer,AttendenceSerializer
from .permissions import OnlyAdminPermission,OnlyAdminCanUpdateOrDelete
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class ShiftViewSet(viewsets.ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    permission_classes = [OnlyAdminPermission]

class BreakViewSet(viewsets.ModelViewSet):
    queryset = Break.objects.all()
    serializer_class = BreakSerializer
    permission_classes = [OnlyAdminPermission]


class UserShiftViewSet(viewsets.ModelViewSet):
    queryset = UserShift.objects.all()
    serializer_class = UserShiftSerializer
    permission_classes = [OnlyAdminPermission]

class AttendenceViewset(viewsets.ModelViewSet):
    serializer_class = AttendenceSerializer
    permission_classes = [IsAuthenticated,OnlyAdminCanUpdateOrDelete]
    http_method_names = ("get", "post", "patch", "delete")

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            # queryset just for schema generation metadata
            return UserShift.objects.none()
        if self.request.user.role != "admin":
            return Attendence.objects.filter(user = self.request.user)

        return Attendence.objects.all().order_by('-date')
