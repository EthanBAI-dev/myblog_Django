from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author_name', 'body']
        labels = {
            'author_name': '你的名字',
            'body': '评论内容',
        }
        widgets = {
            'author_name': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': '请输入你的名字'
            }),
            'body': forms.Textarea(attrs={
                'class': 'textarea-field',
                'placeholder': '写下你的想法…',
                'rows': 5
            }),
        }