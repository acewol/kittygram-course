from django.contrib import admin

from .models import BlogPost, Comment


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'cat',
        'author',
        'is_published',
        'created_at',
    )
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'text', 'author__username', 'cat__name')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'post',
        'author',
        'is_moderated',
        'created_at',
    )
    list_filter = ('is_moderated', 'created_at')
    search_fields = ('text', 'author__username', 'post__title')