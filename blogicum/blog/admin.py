from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Comment, Location, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'created_at')
    list_editable = ('is_published',)
    list_filter = ('is_published',)
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published', 'created_at')
    list_editable = ('is_published',)
    list_filter = ('is_published',)
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'author', 'category', 'location',
        'pub_date', 'is_published', 'image_preview',
    )
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category', 'location', 'author')
    search_fields = ('title', 'text')
    list_select_related = ('author', 'category', 'location')
    date_hierarchy = 'pub_date'
    readonly_fields = ('created_at', 'image_preview')
    fieldsets = (
        (None, {
            'fields': ('title', 'text'),
        }),
        ('Публикация', {
            'fields': ('pub_date', 'is_published', 'created_at'),
        }),
        ('Категория и местоположение', {
            'fields': ('category', 'location'),
        }),
        ('Автор и изображение', {
            'fields': ('author', 'image'),
        }),
        ('Превью изображения', {
            'fields': ('image_preview',),
        }),
    )

    @admin.display(description='Миниатюра')
    def image_preview(self, obj):
        """Показать миниатюру, если у поста есть изображение."""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px;" />',
                obj.image.url,
            )
        return '—'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Админка комментариев: модерация через is_published."""

    list_display = (
        'text_preview', 'post', 'author', 'is_published', 'created_at',
    )
    list_editable = ('is_published',)
    list_filter = ('is_published', 'author', 'created_at')
    search_fields = ('text', 'author__username')
    list_select_related = ('post', 'author')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('text',),
        }),
        ('Связи', {
            'fields': ('post', 'author'),
        }),
        ('Публикация', {
            'fields': ('is_published', 'created_at'),
        }),
    )

    @admin.display(description='Текст')
    def text_preview(self, obj):
        """Первые 60 символов текста — чтобы список был компактным."""
        if len(obj.text) > 60:
            return f'{obj.text[:60]}…'
        return obj.text
