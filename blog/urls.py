from django.urls import path
from . import views
from .views import PostListView

app_name = 'blog'
urlpatterns = [
    # 首页
    path("", PostListView.as_view(), name="post_list"),
    # 分类筛选列表
    path("category/<str:category_slug>/", PostListView.as_view(), name="category_list"),
    # 文章详情
    path('post/<str:slug>/', views.post_detail, name='post_detail'),
    # About 页
    path('about/', views.about, name='about'),
]
