from django.urls import path
from . import views

urlpatterns  = [
    path('assigned-items',views.UserItemAssignmentAPI.as_view()),
]