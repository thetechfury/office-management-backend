from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
shift_router = DefaultRouter()
break_router = DefaultRouter()
user_shift_router = DefaultRouter()
router.register('', views.AttendenceViewset, basename='attendence')

urlpatterns =[
    path("",include(router.urls)),

]
