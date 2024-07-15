from rest_framework.permissions import BasePermission
from rest_framework.validators import ValidationError

class OnlyAdminUserCanMakePostRequest(BasePermission):
    # Only for POST  Request permitted user is admin
    def has_permission(self, request, view):
        if request.method == "POST":
            return request.user.role == "admin"
        return True

class OnlyAdminUserAndInventoryManagerCanMakePostRequest(BasePermission):
    # Only for POST  Request permitted user is admin
    def has_permission(self, request, view):
        if request.method == "POST":
            return request.user.role == "admin" or request.user.role == "inventory_manager"
        return True

class TeamPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin" or obj.leader == request.user:
            return True
        # if request.method == 'GET' and Team.objects.get(leader = request.user):
        #     return True
        else:
            return False



class MembershipPermission(BasePermission):
    def check_team_leader_requested(self,request):
        try:
            team_id = request.data.get('team')
            team_object = Team.objects.get(id=team_id)
            if request.user == team_object.leader:
                return True
            else:
                return False
        except:
            return ValidationError("Only Team Leader can request for data")

    def has_permission(self, request, view):
        # is_team_leader = self.check_team_leader_requested(request)
        # if is_team_leader:
        #     return True
        # else:
        #     return False


        pass



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