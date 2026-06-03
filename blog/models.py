from django.db import models
from django.utils.text import slugify
from mdeditor.fields import MDTextField
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User
from comments.models import Comment

class Category(models.Model):
    name = models.CharField('分类名', max_length=50, unique=True)
    slug = models.SlugField(
        'URL 别名',
        max_length=80,
        unique=True,
        blank=True,
        allow_unicode=True
    )

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField('标签名', max_length=30, unique=True)
    slug = models.SlugField(
        'URL 别名',
        max_length=50,
        unique=True,
        blank=True,
        allow_unicode=True
    )

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('published', '已发布'),
    )

    title = models.CharField('标题', max_length=200)
    slug = models.SlugField(
        'URL 别名',
        max_length=250,
        unique=True,
        blank=True,
        allow_unicode=True,
        help_text='可不填，保存时自动根据标题生成。也可以手动输入英文字母、数字和连字符。'
    )
    excerpt = models.TextField('文章摘要', blank=True, help_text='可选，支持多行输入。如果不填，则前端不显示摘要。')
    cover = models.ImageField(upload_to='post_covers/', blank=True, null=True, verbose_name='文章封面')
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='作者',
        null=True,
    )
    
    content = MDTextField('正文')

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='分类'
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='posts',
        verbose_name='标签'
    )

    created_at = models.DateTimeField('发布时间', auto_now_add=True)
    status = models.CharField(
        '状态',
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )
    views = models.PositiveIntegerField('浏览量', default=0)

    # 添加通用关系，方便在模板中通过 post.comments.all 获取评论
    comments = GenericRelation(Comment)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def reading_time(self):
        """估算阅读时间，假设阅读速度为 400 字/分钟"""
        if not self.content:
            return 1
        import re
        from django.utils.html import strip_tags
        # 去除 HTML 标签
        clean_text = strip_tags(self.content)
        # 简单去除 Markdown 标记
        clean_text = re.sub(r'[#*>_\[\]()`-]', '', clean_text)
        word_count = len(clean_text)
        time = round(word_count / 400)
        return time if time > 0 else 1


class SitePage(models.Model):
    """
    用于站点的单页内容：About / Now / Uses 等
    先实现 about：slug=about
    """
    title = models.CharField('页面标题', max_length=120, default='About')
    slug = models.SlugField('URL 别名', max_length=60, unique=True, allow_unicode=True)
    content = MDTextField('正文（Markdown）', blank=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '站点单页'
        verbose_name_plural = '站点单页'
        ordering = ['slug']

    def __str__(self):
        return self.title