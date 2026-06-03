from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'body_short', 'user', 'author_name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('body', 'author_name', 'author_email', 'user__username')
    list_editable = ('is_active',)
    actions = ['approve_comments']

    def body_short(self, obj):
        return obj.body[:40] + ('...' if len(obj.body) > 40 else '')
    body_short.short_description = '评论内容'

    def approve_comments(self, request, queryset):
        queryset.update(is_active=True)
    approve_comments.short_description = '批量审核通过'
