from django import forms
from .models import Promise, Promise_Comment
from tempus_dominus.widgets import DateTimePicker
from django.utils import timezone

class PromiseForm(forms.ModelForm):

    class Meta:
        model = Promise
        fields = ['title', 'content']

        labels = {
            'title': '제목',
            'content': '약속내용',
        }

class Promise_CommentForm(forms.ModelForm):
    class Meta:
        model = Promise_Comment
        fields = ['content']

        labels = {
            'content': '댓글내용'
        }