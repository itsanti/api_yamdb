from rest_framework import permissions

from .models import User


class IsAdmin(permissions.BasePermission):
    """Вход только для админа."""

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated
                    and request.user.is_admin)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Вход только для чтения, редактирование только для админа."""

    def has_permission(self, request, view):
        return bool((request.method in permissions.SAFE_METHODS)
                    or (request.user.is_authenticated
                        and request.user.is_admin))

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_admin


class IsStaffOrReadOnly(permissions.BasePermission):
    """Вход только для чтения.

    Редактирование только для админа или модератора.
    """

    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_authenticated
                    and ((request.user == obj.author)
                         or (request.user.role in (User.ADMIN, User.MODER))))


class IsAuthorOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )
