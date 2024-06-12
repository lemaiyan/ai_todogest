from django.contrib import admin
from .models import TodoItem, Category, Priority, EmailDigest


@admin.register(TodoItem)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'completed', 'category', 'priority', 'due_date', 'created_at', 'updated_at')
    list_filter = ('completed',)
    search_fields = ('title', 'description')
    ordering = ('completed',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    ordering = ('name',)
    
@admin.register(EmailDigest)
class EmailDigestAdmin(admin.ModelAdmin):
    list_display = ('user', 'summary', 'read', 'created_at')
    search_fields = ('user', 'summary')
    ordering = ('user',)
