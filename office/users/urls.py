from django.urls import path
from . import views

urlpatterns = [
    path("user/update-password/",views.UpdatePasswordAPI.as_view()),
    path("auth/login/",views.LoginAPI.as_view()),
    path("auth/logout/",views.LogoutAPI.as_view()),
    path('user/<user_id>/profile',views.GetUserProfile.as_view()),
    path('user/<user_id>/address',views.GetUserAddress.as_view()),
    path('user/<user_id>/experience',views.GetUserExperience.as_view()),
    path('user/<user_id>/education',views.GetUserEducation.as_view()),

]