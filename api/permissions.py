from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Читать могут все пользователи.
    Изменять и удалять объект может только владелец.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user