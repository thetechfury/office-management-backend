from rest_framework.viewsets import ModelViewSet
from .models import ItemCategory, Item, StockMovement,UserItemAssignment
from .serializers import ItemCategorySerializer, ItemSerializer, StockMovementSerializer, UserItemAssignmentSerializer, \
    ItemPartialUpdateSerializer
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .permissions import ItemPermission
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator

# Create your views here.



class ItemCategoryViewset(ModelViewSet):
    queryset = ItemCategory.objects.all()
    serializer_class = ItemCategorySerializer
    http_method_names = ("get","post","patch","delete")
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,ItemPermission]












class ItemViewset(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    http_method_names = ("get", "post", "patch", "delete")
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,ItemPermission]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return ItemPartialUpdateSerializer
        return ItemSerializer


    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ItemPartialUpdateSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)



class StockMovementViewset(ModelViewSet):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    http_method_names = ("get", "post")
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, ItemPermission]




@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="Assigned Items"
))
class UserItemAssignmentAPI(ListAPIView):
    queryset = UserItemAssignment.objects.all()
    serializer_class = UserItemAssignmentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    http_method_names = ("get")

    def get_queryset(self):
        user = self.request.user
        if user.role  not in ['admin','inventory_manager']:
            return  UserItemAssignment.objects.filter(user_id = user.id)
        else:
            return UserItemAssignment.objects.all()

