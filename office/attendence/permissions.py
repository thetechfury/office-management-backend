from rest_framework.permissions import BasePermission

class OnlyAdminPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'admin':
            return True
        return False

class OnlyAdminCanUpdateOrDelete(BasePermission):
    def has_permission(self, request, view):
        if request.method in ["PATCH","DELETE"] :
           return request.user.role == "admin"
        return True


