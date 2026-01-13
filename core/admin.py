from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Link, Click

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'username')
    ordering = ('email',)

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('short_code', 'original_url', 'owner', 'clicks_count', 'created_at')
    search_fields = ('short_code', 'original_url')
    list_filter = ('created_at', 'owner')

@admin.register(Click)
class ClickAdmin(admin.ModelAdmin):
    list_display = ('link', 'timestamp', 'ip_address', 'referer')
    list_filter = ('timestamp',)
