from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, EmailVerifyRecord

# 取消内置 User 的默认注册
admin.site.unregister(User)


class UserProfileInline(admin.StackedInline):
    """内联显示 UserProfile，纵向排列"""
    model = UserProfile


class UserProfileAdmin(UserAdmin):
    """重新注册 User，内联 UserProfile"""
    inlines = [UserProfileInline]


admin.site.register(User, UserProfileAdmin)


@admin.register(EmailVerifyRecord)
class EmailVerifyRecordAdmin(admin.ModelAdmin):
    list_display = ('code', 'email', 'send_type')
