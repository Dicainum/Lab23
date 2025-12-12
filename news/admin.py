# news/admin.py
from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at", "is_published")
    list_filter = ("is_published", "created_at", "author")
    search_fields = ("title", "content", "author__username")
    readonly_fields = ("created_at", "updated_at")