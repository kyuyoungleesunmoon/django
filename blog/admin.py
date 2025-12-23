from django.contrib import admin
from .models import Category, Tag, Post, Comment, Like, Bookmark

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'views', 'published', 'created_at']
    list_filter = ['published', 'category', 'created_at']
    search_fields = ['title', 'author__username', 'content']
    filter_horizontal = ['tags']
    readonly_fields = ['created_at', 'updated_at', 'views']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('title', 'author', 'category')
        }),
        ('내용', {
            'fields': ('content', 'tags')
        }),
        ('상태', {
            'fields': ('published', 'views')
        }),
        ('날짜', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['author__username', 'post__title', 'content']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__title']

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__title']

