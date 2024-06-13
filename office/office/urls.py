"""
URL configuration for office project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from users import views
from .swagger import swagger_info
# swagger
schema_view = get_schema_view(
    swagger_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# routers
user_router = DefaultRouter()
team_router = DefaultRouter()
membership_router = DefaultRouter()
profile_router = DefaultRouter()
profile_image_router = DefaultRouter()
profile_skill_router = DefaultRouter()
user_router.register('', views.UserViewset, basename='user')
team_router.register('',views.TeamViewset,basename='team')
membership_router.register('',views. MembershipViewset,basename='member')
profile_router.register('',views.ProfileViewset,basename='profile')
profile_image_router.register('',views.ProfileImageViewset,basename='profile')
profile_skill_router.register('',views.ProfileSkillViewset,basename='skill')


urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/",include(user_router.urls)),
    path("team/",include(team_router.urls)),
    path("member/",include(membership_router.urls)),
    path("profile/",include(profile_router.urls)),
    path("profile-image/",include(profile_image_router.urls)),
    path("profile-skill/",include(profile_skill_router.urls)),
    path("",include('users.urls')),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]+static(settings.MEDIA_URL,
         document_root=settings.MEDIA_ROOT)

