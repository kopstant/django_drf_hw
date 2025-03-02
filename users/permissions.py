from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Проверяет принадлежит ли пользователь группе "moderator"
        Если пользователь в группе модератов, он получается доступ к View.(CourseView or LessonViewSet).
        """
        return request.user.groups.filter(name='moderator').exists()

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
        Проверяем, является ли пользователь модератором или владельцем объекта
        """
        return IsModerator().has_permission(request, view) or IsOwner().has_object_permission(request, view, obj)
