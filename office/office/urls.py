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
from inventory import views as inventory_views
from attendence import views as attendence_view
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
profile_education_router = DefaultRouter()
working_experience_router = DefaultRouter()
address_router = DefaultRouter()
inventory_category_router = DefaultRouter()
inventory_item_router = DefaultRouter()
inventory_stock_movment_router = DefaultRouter()
break_router = DefaultRouter()
user_shift_router = DefaultRouter()
user_router.register('', views.UserViewset, basename='user')
team_router.register('',views.TeamViewset,basename='team')
membership_router.register('',views. MembershipViewset,basename='member')
profile_router.register('',views.ProfileViewset,basename='profile')
profile_education_router.register('',views.ProfileEducationViewset,basename='profile-education')
profile_image_router.register('',views.ProfileImageViewset,basename='profile')
profile_skill_router.register('',views.ProfileSkillViewset,basename='skill')
address_router.register('',views.ProfileAddressViewset,basename='address')
working_experience_router.register('',views.WorkingExperienceViewset,basename='experience')
inventory_category_router.register('',inventory_views.ItemCategoryViewset,basename='inventory')
inventory_item_router.register('',inventory_views.ItemViewset,basename='inventory')
inventory_stock_movment_router.register('',inventory_views.StockMovementViewset,basename='inventory')
break_router.register('',attendence_view.BreakViewSet,basename='shift-break')
user_shift_router.register('',attendence_view.UserShiftViewSet,basename='shift-break')


urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/",include(user_router.urls)),
    path("team/",include(team_router.urls)),
    path("member/",include(membership_router.urls)),
    path("profile/",include(profile_router.urls)),
    path("profile-image/",include(profile_image_router.urls)),
    path("profile-education/",include(profile_education_router.urls)),
    path("profile-skill/",include(profile_skill_router.urls)),
    path("profile-address/",include(address_router.urls)),
    path("work-experience/",include(working_experience_router.urls)),
    path("inventory-item-category/",include(inventory_category_router.urls)),
    path("inventory-item/",include(inventory_item_router.urls)),
    path("inventory-stock-movemnet/",include(inventory_stock_movment_router.urls)),
    path("shift-break/",include(break_router.urls)),
    path("user-shift/",include(user_shift_router.urls)),
    path("",include('users.urls')),
    path("attendece/",include('attendence.urls')),
    path("inventory/",include('inventory.urls')),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]+static(settings.MEDIA_URL,
         document_root=settings.MEDIA_ROOT)

