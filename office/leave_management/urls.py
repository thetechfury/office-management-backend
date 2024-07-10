from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
# leave_application_router = DefaultRouter()
user_leave_router = DefaultRouter()
# leave_application_router.register('', views.LeaveApplicationViewset, basename='leave')
user_leave_router.register('', views.UserLeavesViewset, basename='user-leave')

urlpatterns =[
    path("",include(user_leave_router.urls)),
    # path("user-leaves/",include(user_leave_router.urls))

]
