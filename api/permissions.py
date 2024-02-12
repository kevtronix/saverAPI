from rest_framework import permissions
from guardian.shortcuts import get_objects_for_user


class IsRestaurant(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('api.restaurant')
    
class IsShelter(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('api.shelter')

class IsFoodInspector(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('api.inspector')

class IsVolunteer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('api.volunteer')

class IsOrganizer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('api.organizer')