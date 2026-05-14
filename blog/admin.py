from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Post, Category, Tag, SitePage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'created_at', 'views')
    list_filter = ('status', 'category', 'tags', 'created_at')
    search_fields = ('title', 'content')
    filter_horizontal = ('tags',)




@admin.register(SitePage)
class SitePageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'updated_at')
    search_fields = ('title', 'slug', 'content')
    prepopulated_fields = {'slug': ('title',)}