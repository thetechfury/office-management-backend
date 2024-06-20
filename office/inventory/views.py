from rest_framework.viewsets import ModelViewSet
from .models import ItemCategory,Item
from .serializers import ItemCategorySerializer,ItemSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
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

