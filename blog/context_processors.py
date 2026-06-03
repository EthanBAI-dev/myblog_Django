from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from blog.models import Post


def sidebar_context(request):
    """全局侧边栏数据：最新文章、热门文章、归档"""
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

    return {
        'sidebar_recent_posts': recent_posts,
        'sidebar_hot_posts': hot_posts,
        'sidebar_archives': archives,
    }
