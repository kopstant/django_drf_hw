from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Проверяет доступ к конкретному объекту.
        """
        return request.user.groups.filter(name='moderator').exists()


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Проверяет право доступа к конкретному объекту
        """
        return obj.owner == request.user


class IsModeratorOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.owner == request.user
