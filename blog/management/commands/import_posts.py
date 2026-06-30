"""
将项目中的 .md 文档导入为博客文章。

用法:
    python manage.py import_posts

该命令会读取 articles/ 目录下的 markdown 文件，
转换为 HTML 后创建为已发布的 Post 对象。
"""

import markdown
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Post, Category, Tag

# 要导入的文档: (文件路径(相对于 BASE_DIR), 标题, 分类名, [标签列表])
POSTS_TO_IMPORT = [
    {
        'file': 'articles/zh-hans/部署指南.md',
        'title': 'Django 博客部署指南：从零到自动更新',
        'category': '技术',
        'tags': ['Django', '部署', 'PythonAnywhere', 'GitHub Actions'],
    },
    {
        'file': 'articles/zh-hans/个人网站制作教程.md',
        'title': '个人网站制作教程：从想法到上线',
        'category': '教程',
        'tags': ['个人网站', 'Vibe Coding', '前端', '入门'],
    },
    {
        'file': 'articles/zh-hans/多语言维护规则.md',
        'title': '用 Vibe Coding 做多语言网站，我是怎么用一条规则解决翻译混乱的',
        'category': '经验',
        'tags': ['Vibe Coding', 'i18n', '多语言', '工作流'],
    },
]

MD_EXTENSIONS = [
    'markdown.extensions.fenced_code',
    'markdown.extensions.codehilite',
    'markdown.extensions.tables',
    'markdown.extensions.nl2br',
]


class Command(BaseCommand):
    help = '将 articles/ 中的 .md 文档导入为博客文章'

    def handle(self, *args, **options):
        import os
        from django.conf import settings

        base_dir = settings.BASE_DIR

        # 获取第一个超级用户作为作者
        author = User.objects.filter(is_superuser=True).first()
        if not author:
            self.stdout.write(self.style.ERROR('没有找到超级用户，请先创建：python manage.py createsuperuser'))
            return
        self.stdout.write(f'使用作者: {author.username}')

        count = 0
        for post_info in POSTS_TO_IMPORT:
            file_path = os.path.join(base_dir, post_info['file'])
            title = post_info['title']

            if not os.path.exists(file_path):
                self.stdout.write(self.style.WARNING(f'文件不存在，跳过: {file_path}'))
                continue

            if Post.objects.filter(title=title).exists():
                self.stdout.write(f'文章已存在，跳过: {title}')
                continue

            with open(file_path, 'r', encoding='utf-8') as f:
                md_content = f.read()

            html_content = markdown.markdown(md_content, extensions=MD_EXTENSIONS)
            category, _ = Category.objects.get_or_create(name=post_info['category'])

            post = Post.objects.create(
                title=title,
                content=html_content,
                category=category,
                author=author,
                status='published',
            )

            for tag_name in post_info['tags']:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                post.tags.add(tag)

            self.stdout.write(self.style.SUCCESS(f'已导入: {title}'))
            count += 1

        self.stdout.write(self.style.SUCCESS(f'全部导入完成！共导入 {count} 篇文章'))
