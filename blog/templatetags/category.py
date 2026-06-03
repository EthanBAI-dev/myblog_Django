from django import template
from blog.models import Category

register = template.Library()


@register.simple_tag
def get_category_list():
    """获取全站分类列表，供导航栏全局调用"""
    return Category.objects.all()
