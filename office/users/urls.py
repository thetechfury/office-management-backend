from django.urls import path,include

from rest_framework.routers import DefaultRouter

from . import views

user_router = DefaultRouter()
user_router.register('', views.UserViewset, basename='user')
urlpatterns = [
    path("user/update-password/",views.UpdatePasswordAPI.as_view()),
    path("auth/login/",views.LoginAPI.as_view()),
    path("auth/logout/",views.LogoutAPI.as_view()),
    path('user/users-select-list/', views.GetuserForAsForeignKey.as_view()),
    path('user/<user_id>/profile/',views.GetUserProfile.as_view()),
    path('user/<user_id>/address/',views.GetUserAddress.as_view()),
    path('user/<user_id>/experience/',views.GetUserExperience.as_view()),
    path('user/<user_id>/education/',views.GetUserEducation.as_view()),
    path('user/<user_id>/skills/',views.GetUserSkills.as_view()),
    path('user/<user_id>/teams/',views.GetUserTeams.as_view()),
    path("user/",include(user_router.urls)),

]