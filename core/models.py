from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from .utils import encode

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class Link(models.Model):
    original_url = models.URLField(max_length=2000)
    short_code = models.CharField(max_length=15, unique=True, blank=True, null=True, db_index=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='links',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    clicks_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.short_code:
            # Save first to get an ID for encoding if not provided
            # Note: This is a simple approach. A more robust one might use a UUID or a pre-defined sequence.
            super().save(*args, **kwargs)
            self.short_code = encode(self.id)
            kwargs['force_insert'] = False # Ensure we update the existing record
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"

    class Meta:
        ordering = ['-created_at']

class Click(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name='clicks')
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, null=True, blank=True)
    referer = models.URLField(max_length=1000, null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Click on {self.link.short_code} at {self.timestamp}"
