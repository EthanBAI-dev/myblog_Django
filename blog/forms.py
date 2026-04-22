from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # 只需要让用户输入昵称和内容，文章关联由后台自动处理
        fields = ['author_name', 'body']
        widgets = {
            'author_name': forms.TextInput(attrs={'placeholder': '您的昵称', 'class': 'form-control'}),
            'body': forms.Textarea(attrs={'placeholder': '写下您的评论...', 'class': 'form-control', 'rows': 4}),
        }