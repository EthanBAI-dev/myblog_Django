from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from django.contrib.auth.models import User
from users.models import UserProfile
from blog.models import Post


def sidebar_context(request):
    """全局侧边栏数据：博主信息、最新文章、热门文章、归档"""
    published = Post.objects.filter(status='published')

    # 最新文章（最近 5 篇）
    recent_posts = published.order_by('-created_at')[:5]

    # 热门文章：优先推荐，再按浏览量降序
    hot_posts = published.order_by('-is_recommended', '-views')[:5]

    # 按月归档
    archives = (
        published
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('-month')
    )

    # 博主信息：取第一个超级管理员
    blog_owner = None
    try:
        owner_user = User.objects.filter(is_superuser=True).first()
        if owner_user:
            blog_owner = UserProfile.objects.filter(owner=owner_user).first()
    except Exception:
        pass

    return {
        'sidebar_recent_posts': recent_posts,
        'sidebar_hot_posts': hot_posts,
        'sidebar_archives': archives,
        'blog_owner': blog_owner,
    }
