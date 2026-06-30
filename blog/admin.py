from django.contrib import admin
from .models import Post, Category, Tag, SitePage, HomePage


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
    list_display = ('title', 'category', 'language', 'status', 'created_at', 'views')
    list_filter = ('status', 'language', 'category', 'tags', 'created_at')
    search_fields = ('title', 'content')
    filter_horizontal = ('tags',)




@admin.register(SitePage)
class SitePageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'updated_at')
    search_fields = ('title', 'slug', 'content')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'updated_at')
    fieldsets = (
        ('Hero 区域', {
            'fields': ('slogan', 'hero_sub')
        }),
        ('卡片内容', {
            'fields': ('about_me', 'current_work', 'skills_text', 'hobbies')
        }),
    )

    def has_add_permission(self, request):
        """只允许一个 HomePage 记录"""
        if HomePage.objects.exists():
            return False
        return True