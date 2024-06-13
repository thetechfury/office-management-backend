from django.urls import path
from . import views

urlpatterns = [
    path("user/update-password/",views.UpdatePasswordAPI.as_view()),
    path("auth/login/",views.LoginAPI.as_view()),
    path("auth/logout/",views.LogoutAPI.as_view()),

]