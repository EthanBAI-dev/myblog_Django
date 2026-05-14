from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # 由于是通用的模型，先只暴露这两个基础字段
        fields = ['author_name', 'body']
        labels = {
            'author_name': '你的名字',
            'body': '评论内容',
        }
        widgets = {
            'author_name': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': '请输入你的名字（游客）'
            }),
            'body': forms.Textarea(attrs={
                'class': 'textarea-field',
                'placeholder': '写下你的想法…',
                'rows': 5
            }),
        }
