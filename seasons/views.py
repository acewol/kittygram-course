from django.utils import timezone
from rest_framework import decorators, permissions, response, status, viewsets

from .models import Season, SeasonResult
from .permissions import IsAdminOrReadOnly
from .serializers import (
    AddPointsSerializer,
    LeaderboardSerializer,
    SeasonResultSerializer,
    SeasonSerializer,
)


class SeasonViewSet(viewsets.ModelViewSet):
    serializer_class = SeasonSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_fields = ('is_active', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    ordering_fields = ('start_date', 'end_date', 'created_at', 'title')

    def get_queryset(self):
        return Season.objects.prefetch_related('results')

    @decorators.action(
        detail=True,
        methods=['post'],
        permission_classes=(permissions.IsAdminUser,),
    )
    def activate(self, request, pk=None):
        season = self.get_object()
        today = timezone.localdate()

        if season.end_date < today:
            return response.Response(
                {'detail': 'Нельзя активировать завершенный сезон.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Season.objects.exclude(id=season.id).update(is_active=False)
        season.is_active = True
        season.save()

        serializer = self.get_serializer(season)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    @decorators.action(
        detail=True,
        methods=['post'],
        permission_classes=(permissions.IsAdminUser,),
    )
    def add_points(self, request, pk=None):
        season = self.get_object()

        if not season.is_active:
            return response.Response(
                {'detail': 'Начислять очки можно только в активном сезоне.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = AddPointsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        points = serializer.validated_data['points']
        action = serializer.validated_data['action']

        result, _ = SeasonResult.objects.get_or_create(
            season=season,
            user=user,
        )
        result.points += points
        result.last_action = action
        result.save()

        result_serializer = SeasonResultSerializer(result)
        return response.Response(
            result_serializer.data,
            status=status.HTTP_200_OK,
        )

    @decorators.action(
        detail=True,
        methods=['get'],
        permission_classes=(permissions.AllowAny,),
    )
    def leaderboard(self, request, pk=None):
        season = self.get_object()
        queryset = SeasonResult.objects.select_related(
            'season',
            'user',
        ).filter(
            season=season
        ).order_by(
            '-points',
            'updated_at'
        )

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = LeaderboardSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = LeaderboardSerializer(queryset, many=True)
        return response.Response(serializer.data)


class SeasonResultViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SeasonResultSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filterset_fields = ('season', 'season__title')
    search_fields = ('season__title', 'last_action')
    ordering_fields = ('points', 'updated_at')

    def get_queryset(self):
        queryset = SeasonResult.objects.select_related(
            'season',
            'user',
        )

        if self.request.user.is_staff:
            return queryset

        return queryset.filter(user=self.request.user)