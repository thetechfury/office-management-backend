from rest_framework.permissions import BasePermission

class ItemPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'admin' or request.user.role =='inventory_manager':
            return True
        else:
            return False