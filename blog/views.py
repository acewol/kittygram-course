from django.db.models import Count
from rest_framework import decorators, permissions, response, status, viewsets

from .models import BlogPost, Comment
from .permissions import (
    IsAuthorOrReadOnly,
    IsCommentAuthorOrPostAuthorOrReadOnly,
)
from .serializers import (
    BlogPostDetailSerializer,
    BlogPostSerializer,
    CommentSerializer,
)


class BlogPostViewSet(viewsets.ModelViewSet):
    serializer_class = BlogPostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    )
    filterset_fields = (
        'cat',
        'cat__name',
        'author__username',
        'is_published',
    )
    search_fields = (
        'title',
        'text',
        'cat__name',
        'author__username',
    )
    ordering_fields = (
        'created_at',
        'updated_at',
        'title',
    )

    def get_queryset(self):
        queryset = BlogPost.objects.select_related(
            'author',
            'cat',
        ).prefetch_related(
            'comments'
        ).annotate(
            comments_total=Count('comments')
        )

        user = self.request.user

        if user.is_authenticated:
            return queryset.filter(is_published=True) | queryset.filter(
                author=user
            )

        return queryset.filter(is_published=True)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BlogPostDetailSerializer
        return BlogPostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @decorators.action(
        detail=True,
        methods=['post'],
        permission_classes=(permissions.IsAuthenticated, IsAuthorOrReadOnly),
    )
    def toggle_publish(self, request, pk=None):
        post = self.get_object()
        post.is_published = not post.is_published
        post.save()

        serializer = self.get_serializer(post)
        return response.Response(serializer.data)

    @decorators.action(
        detail=True,
        methods=['get', 'post'],
        permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
    )
    def comments(self, request, pk=None):
        post = self.get_object()

        if request.method == 'GET':
            comments = post.comments.select_related('author')
            page = self.paginate_queryset(comments)

            if page is not None:
                serializer = CommentSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = CommentSerializer(comments, many=True)
            return response.Response(serializer.data)

        serializer = CommentSerializer(
            data={
                'post': post.id,
                'text': request.data.get('text'),
            },
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user, post=post)

        return response.Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsCommentAuthorOrPostAuthorOrReadOnly,
    )
    filterset_fields = (
        'post',
        'post__cat',
        'author__username',
        'is_moderated',
    )
    search_fields = (
        'text',
        'post__title',
        'author__username',
    )
    ordering_fields = (
        'created_at',
        'updated_at',
    )

    def get_queryset(self):
        queryset = Comment.objects.select_related(
            'post',
            'author',
            'post__author',
            'post__cat',
        )

        user = self.request.user

        if user.is_authenticated:
            return queryset.filter(post__is_published=True) | queryset.filter(
                post__author=user
            )

        return queryset.filter(post__is_published=True)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @decorators.action(
        detail=True,
        methods=['post'],
        permission_classes=(
            permissions.IsAuthenticated,
            IsCommentAuthorOrPostAuthorOrReadOnly,
        ),
    )
    def moderate(self, request, pk=None):
        comment = self.get_object()
        comment.is_moderated = True
        comment.save()

        serializer = self.get_serializer(comment)
        return response.Response(serializer.data)