from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Season, SeasonResult


User = get_user_model()


class SeasonSerializer(serializers.ModelSerializer):
    results_count = serializers.SerializerMethodField()

    class Meta:
        model = Season
        fields = (
            'id',
            'title',
            'description',
            'start_date',
            'end_date',
            'is_active',
            'results_count',
            'created_at',
        )
        read_only_fields = ('is_active', 'results_count', 'created_at')

    def get_results_count(self, obj):
        return obj.results.count()

    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError(
                'Дата начала сезона не может быть позже даты окончания.'
            )

        return attrs


class SeasonResultSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    season_title = serializers.CharField(
        source='season.title',
        read_only=True
    )

    class Meta:
        model = SeasonResult
        fields = (
            'id',
            'season',
            'season_title',
            'user',
            'points',
            'last_action',
            'updated_at',
        )
        read_only_fields = (
            'season',
            'season_title',
            'user',
            'points',
            'last_action',
            'updated_at',
        )


class AddPointsSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    points = serializers.IntegerField(
        min_value=1,
        max_value=100
    )
    action = serializers.CharField(
        max_length=120
    )

    def validate_action(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                'Описание действия должно содержать минимум 3 символа.'
            )
        return value


class LeaderboardSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    season_title = serializers.CharField(
        source='season.title',
        read_only=True
    )

    class Meta:
        model = SeasonResult
        fields = (
            'id',
            'season_title',
            'user',
            'points',
            'last_action',
            'updated_at',
        )