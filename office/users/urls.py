from django.urls import path
from . import views

urlpatterns = [
    path("user/update-password/",views.UpdatePasswordAPI.as_view())
]