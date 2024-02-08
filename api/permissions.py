from rest_framework import permissions
from guardian.shortcuts import get_objects_for_user

class CustomObjectPermissions(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):
        # General permissions check, e.g., is user authenticated?
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check permissions for read actions
        if request.method in permissions.SAFE_METHODS:
            return request.user.has_perm('view_' + obj._meta.model_name, obj)

        # Check permissions for write actions
        elif request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user.has_perm('change_' + obj._meta.model_name, obj) or \
                   request.user.has_perm('delete_' + obj._meta.model_name, obj)


class IsSpecialist(permissions.BasePermission):
    def has_permissions(self, request, view):
        return request.user.has_perm('api.specialist')


class IsVolunteer(permissions.BasePermission):
    def has_permissions(self, request, view):
        return request.user.has_perm('api.volunteer')

class IsOrganizer(permissions.BasePermission):
    def has_permissions(self, request, view):
        return request.user.has_perm('api.organizer')