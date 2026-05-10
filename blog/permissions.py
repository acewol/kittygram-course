from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Читать могут все.
    Изменять и удалять объект может только автор.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class IsCommentAuthorOrPostAuthorOrReadOnly(permissions.BasePermission):
    """
    Читать могут все.
    Изменять комментарий может автор комментария.
    Удалять и модерировать комментарий может автор комментария или автор поста.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method in ('DELETE', 'POST'):
            return obj.author == request.user or obj.post.author == request.user

        return obj.author == request.user