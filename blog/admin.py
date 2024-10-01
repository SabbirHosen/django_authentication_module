from django.contrib import admin
from .models import Blog, Comment

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'content', 'author__email')
    prepopulated_fields = {'slug': ('title',)}  # Automatically fill slug

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'author_name', 'created_at')
    search_fields = ('author_name', 'author_email', 'content')
