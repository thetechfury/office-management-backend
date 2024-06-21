from rest_framework.viewsets import ModelViewSet
from .models import ItemCategory, Item, StockMovement,UserItemAssignment
from .serializers import ItemCategorySerializer,ItemSerializer,StockMovementSerializer,UserItemAssignmentSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .permissions import ItemPermission
# Create your views here.

class ItemCategoryViewset(ModelViewSet):
    queryset = ItemCategory.objects.all()
    serializer_class = ItemCategorySerializer
    http_method_names = ("get","post","patch","delete")
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated,ItemPermission]



class ItemViewset(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    http_method_names = ("get", "post", "patch", "delete")
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated,ItemPermission]




class StockMovementViewset(ModelViewSet):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    http_method_names = ("get", "post")
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, ItemPermission]




class UserItemAssignmentAPI(ListAPIView):
    queryset = UserItemAssignment.objects.all()
    serializer_class = UserItemAssignmentSerializer
    http_method_names = ("get")

