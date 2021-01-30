from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Allows access only to admin users. """
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'ADMIN')


class IsLineManagerOrAdmin(permissions.BasePermission):
    """Allows access admin or line managers. """
    def has_permission(self, request, view):
        return bool(request.user and ((request.user.role == 'ADMIN') or
                                      (request.user.role == 'MANAGER')))
