from django.urls import path
from . import views
from .views import PostListView

app_name = 'blog'
urlpatterns = [
    # 这里的空字符串代表 http://127.0.0.1:8000/
    # 首页：不需要参数

    # 详情页（如果你以后要做）：才需要 <int:pk>
    path('post/<str:slug>/', views.post_detail, name='post_detail'),
    path("", PostListView.as_view(), name="post_list"),
    path('about/', views.about, name='about'),
]