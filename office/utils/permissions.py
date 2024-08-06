from rest_framework.permissions import BasePermission

class OnlyAdminUserCanMakePostRequest(BasePermission):
    # For POST  Request permitted user is admin
    def has_permission(self, request, view):
        if request.method == "POST":
            return request.user.role == "admin"
        return True


class OnlyAdminUserCanGet(BasePermission):
    # Only for POST  Request permitted user is admin
    def has_permission(self, request, view):
        if request.method == "GET":
            return request.user.role == "admin"
        return False

class OnlyAdminUserCanPostAndDelete(BasePermission):
    # Only for POST  Request permitted user is admin
    def has_permission(self, request, view):
        if request.method == "POST" or request.method == "DELETE":
            return request.user.role == "admin"
        return True
class OnlyAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "admin"


class OnlyAdminUserAndInventoryManagerCanMakePostRequest(BasePermission):
    # Only for POST  Request permitted user is admin
    def has_permission(self, request, view):
        if request.method == "POST":
            return request.user.role == "admin" or request.user.role == "inventory_manager"
        return True









class ProfilePermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.user or request.user.role == "admin":
            return True

        else:
            return False


class ItemPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'admin' or request.user.role =='inventory_manager':
            return True
        else:
            return False