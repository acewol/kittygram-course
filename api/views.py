from rest_framework import parsers, permissions, viewsets

from cats.models import Achievement, Cat
from .permissions import IsOwnerOrReadOnly
from .serializers import AchievementSerializer, CatSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    search_fields = ('name',)
    ordering_fields = ('name',)


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.select_related('owner').prefetch_related(
        'achievements'
    )
    serializer_class = CatSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )
    parser_classes = (
        parsers.JSONParser,
        parsers.MultiPartParser,
        parsers.FormParser,
    )
    filterset_fields = ('color', 'birth_year', 'owner__username')
    search_fields = ('name', 'description', 'achievements__name')
    ordering_fields = ('name', 'birth_year', 'created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)