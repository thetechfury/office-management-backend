from rest_framework import viewsets
from .models import Shift,Break,UserShift
from .serializers import ShiftSerializer
from .serializers import BreakSerializer,UserShiftSerializer
from .permissions import OnlyAdminPermission
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