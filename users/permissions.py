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
        """
        Модераторы могут видеть и редактировать все объекты,
        а владельцы могут работать только с собственными объектами.
        """
        # Модераторы могут видеть и редактировать все объекты
        if request.user.groups.filter(name='moderator').exists():
            return True
        # Обычные пользователи могут видеть и редактировать только свои объекты
        return obj.owner == request.user
