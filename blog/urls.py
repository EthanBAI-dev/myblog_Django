from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    # 这里的空字符串代表 http://127.0.0.1:8000/
    # 首页：不需要参数
    path('', views.post_list, name='post_list'),

    # 详情页（如果你以后要做）：才需要 <int:pk>
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
]