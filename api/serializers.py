from datetime import datetime

from rest_framework import serializers

from cats.models import Achievement, Cat


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ('id', 'name')


class CatSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    achievements = AchievementSerializer(
        many=True,
        required=False
    )
    age = serializers.SerializerMethodField()

    class Meta:
        model = Cat
        fields = (
            'id',
            'owner',
            'name',
            'color',
            'birth_year',
            'age',
            'description',
            'image',
            'achievements',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('owner', 'created_at', 'updated_at')

    def get_age(self, obj):
        return datetime.now().year - obj.birth_year

    def validate_name(self, value):
        if value.isdigit():
            raise serializers.ValidationError(
                'Кличка котика не может состоять только из цифр.'
            )
        return value

    def validate_color(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                'Цвет должен содержать минимум 3 символа.'
            )
        return value

    def validate_achievements(self, value):
        if len(value) > 5:
            raise serializers.ValidationError(
                'У одного котика не может быть больше 5 достижений.'
            )
        return value

    def _get_or_create_achievements(self, achievements_data):
        achievements = []

        for achievement_data in achievements_data:
            achievement, _ = Achievement.objects.get_or_create(
                name=achievement_data['name']
            )
            achievements.append(achievement)

        return achievements

    def create(self, validated_data):
        achievements_data = validated_data.pop('achievements', [])
        cat = Cat.objects.create(**validated_data)
        achievements = self._get_or_create_achievements(achievements_data)
        cat.achievements.set(achievements)
        return cat

    def update(self, instance, validated_data):
        achievements_data = validated_data.pop('achievements', None)

        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()

        if achievements_data is not None:
            achievements = self._get_or_create_achievements(achievements_data)
            instance.achievements.set(achievements)

        return instance