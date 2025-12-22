from django.contrib import admin
from .models import Page, About, Contact

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')
    readonly_fields = ('updated_at',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'updated_at')
    readonly_fields = ('updated_at',)

