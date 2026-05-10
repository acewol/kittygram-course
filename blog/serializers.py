from rest_framework import serializers

from cats.models import Cat
from .models import BlogPost, Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'post',
            'author',
            'text',
            'is_moderated',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'author',
            'is_moderated',
            'created_at',
            'updated_at',
        )

    def validate_text(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                'Комментарий должен содержать минимум 3 символа.'
            )
        return value

    def validate(self, attrs):
        post = attrs.get('post')

        if post and not post.is_published:
            request = self.context.get('request')
            if not request or post.author != request.user:
                raise serializers.ValidationError(
                    'Нельзя комментировать неопубликованный пост.'
                )

        return attrs


class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    cat_name = serializers.CharField(
        source='cat.name',
        read_only=True
    )
    comments_count = serializers.IntegerField(
        source='comments.count',
        read_only=True
    )

    class Meta:
        model = BlogPost
        fields = (
            'id',
            'author',
            'cat',
            'cat_name',
            'title',
            'text',
            'is_published',
            'comments_count',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'author',
            'created_at',
            'updated_at',
            'comments_count',
        )

    def validate_title(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError(
                'Заголовок поста должен содержать минимум 5 символов.'
            )
        return value

    def validate_text(self, value):
        if len(value.strip()) < 20:
            raise serializers.ValidationError(
                'Текст поста должен содержать минимум 20 символов.'
            )
        return value

    def validate_cat(self, value):
        request = self.context.get('request')

        if request and value.owner != request.user:
            raise serializers.ValidationError(
                'Нельзя создать пост про чужого котика.'
            )

        return value


class BlogPostDetailSerializer(BlogPostSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta(BlogPostSerializer.Meta):
        fields = BlogPostSerializer.Meta.fields + ('comments',)