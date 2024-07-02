from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('', views.LeaveApplicationViewset, basename='leave')

urlpatterns =[
    path("",include(router.urls)),

]
