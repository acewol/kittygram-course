from django.contrib import admin

from .models import Achievement, Cat


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'birth_year', 'owner')
    list_filter = ('color', 'birth_year')
    search_fields = ('name', 'owner__username')
    filter_horizontal = ('achievements',)