from django.contrib import admin

from .models import Season, SeasonResult


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'start_date',
        'end_date',
        'is_active',
        'created_at',
    )
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('title', 'description')


@admin.register(SeasonResult)
class SeasonResultAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'season',
        'user',
        'points',
        'last_action',
        'updated_at',
    )
    list_filter = ('season', 'updated_at')
    search_fields = ('season__title', 'user__username', 'last_action')