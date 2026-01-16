from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from .models import User, Link, Click

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

@admin.register(Link)
class LinkAdmin(ModelAdmin):
    list_display = ('short_code', 'original_url', 'owner', 'clicks_count', 'created_at')
    search_fields = ('short_code', 'original_url', 'owner__email')
    list_filter = ('created_at', 'owner')
    readonly_fields = ('created_at', 'clicks_count')
    
    # Adding a custom action example
    actions = ['reset_clicks']
    
    @admin.action(description="Reset clicks count to 0")
    def reset_clicks(self, request, queryset):
        queryset.update(clicks_count=0)

@admin.register(Click)
class ClickAdmin(ModelAdmin):
    list_display = ('link', 'timestamp', 'ip_address', 'referer')
    list_filter = ('timestamp', 'link')
    search_fields = ('link__short_code', 'ip_address')
    readonly_fields = ('timestamp', 'link', 'ip_address', 'user_agent', 'referer')
