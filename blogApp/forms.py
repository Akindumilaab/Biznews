from django import forms
from .models import BlogInfo, Comment

class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogInfo
        fields = [
            'title',
            'category',
            'image',
            'content'
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content'
        ]