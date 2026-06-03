from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Comment(models.Model):
    # 1. 通用外键：让评论可以挂载到任何模型上
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # 2. 评论者信息
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='注册用户',
        null=True,
        blank=True
    )
    author_name = models.CharField('游客昵称', max_length=50, blank=True)
    author_email = models.EmailField('游客邮箱', blank=True)

    # 3. 评论内容
    body = models.TextField('评论内容')

    # 4. 嵌套评论（楼中楼）：指向自身的 ForeignKey
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name='回复给'
    )

    # 5. 审核机制：默认 False，后台通过后才显示
    is_active = models.BooleanField('审核通过', default=False)

    created_at = models.DateTimeField('评论时间', auto_now_add=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['created_at']  # 通常楼中楼按时间正序排列比较符合直觉

    def __str__(self):
        name = self.user.username if self.user else (self.author_name or "匿名游客")
        return f"{name} 的评论: {self.body[:20]}"
