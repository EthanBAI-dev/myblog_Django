from django.urls import path
from . import views
from .views import PostListView, SearchListView

app_name = 'blog'
urlpatterns = [
    # 首页（个人名片）
    path("", views.home, name="home"),
    # 博客文章列表
    path("blog/", PostListView.as_view(), name="post_list"),
    # 分类筛选列表
    path("category/<str:category_slug>/", PostListView.as_view(), name="category_list"),
    # 文章详情
    path('post/<str:slug>/', views.post_detail, name='post_detail'),
    # About 页
    path('about/', views.about, name='about'),
    # 搜索
    path('search/', SearchListView.as_view(), name='search'),
    # 简历
    path('resume/', views.resume, name='resume'),
    # 我的作品
    path('portfolio/', views.portfolio, name='portfolio'),
]
