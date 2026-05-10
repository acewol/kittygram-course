from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Читать сезоны могут все.
    Создавать, изменять, активировать сезон и начислять очки может только администратор.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_staff