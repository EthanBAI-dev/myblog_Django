from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
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
    
    content = CKEditor5Field('正文', config_name='default')

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
    is_recommended = models.BooleanField('推荐', default=False, help_text='勾选后该文章将出现在侧边栏推荐区')

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
        # 去除多余空白
        clean_text = re.sub(r'\s+', '', clean_text)
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
    content = CKEditor5Field('正文（富文本）', config_name='default', blank=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '站点单页'
        verbose_name_plural = '站点单页'
        ordering = ['slug']

    def __str__(self):
        return self.title


class HomePage(models.Model):
    """
    首页内容模型 - 将各项内容拆分为独立结构化字段
    """
    slogan = models.CharField('首页标语', max_length=200, default='探索深度学习的边界，用代码构建智能的未来。')
    hero_sub = models.CharField('副标题', max_length=200, blank=True, default='深度学习工程师 & AI 技术探索者 · 持续学习中')
    about_me = CKEditor5Field('关于我', config_name='default', blank=True, help_text='个人介绍，显示在"关于"卡片中')
    current_work = CKEditor5Field('当前工作', config_name='default', blank=True, help_text='当前正在进行的工作/项目，显示在"当下"卡片中')
    skills_text = models.TextField('技能标签', blank=True, default='Python、Django、PyTorch、TensorFlow、NumPy、Pandas、Scikit-learn、Git、HTML/CSS、SQL', help_text='多个技能以中文顿号（、）分隔')
    hobbies = CKEditor5Field('热爱与坚持', config_name='default', blank=True, help_text='兴趣爱好与长期坚持，显示在"热爱 & 坚持"卡片中')
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '首页内容'
        verbose_name_plural = '首页内容'

    def __str__(self):
        return '首页内容'

    def get_skills_list(self):
        """返回技能标签列表"""
        if self.skills_text:
            return [s.strip() for s in self.skills_text.replace(',', '、').split('、') if s.strip()]
        return []