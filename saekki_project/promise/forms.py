from django import forms
from .models import *
from tempus_dominus.widgets import DateTimePicker
from django.utils import timezone

class PromiseForm(forms.ModelForm):

    class Meta:
        model = Promise
        fields = ['title', 'content']

        labels = {
            'title': '제목',
                
            'content': '글내용',
        }

        #form css class, id 입히기

    def __init__(self, *args, **kwargs):
        super(PromiseForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control formInput'
        self.fields['content'].widget.attrs['class'] = 'form-control formInput'

class Promise_CommentForm(forms.ModelForm):
    class Meta:
        model = Promise_Comment
        fields = ['content']

        labels = {
            'content': '댓글내용'
        }
    def __init__(self, *args, **kwargs):
        super(Promise_CommentForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['class'] = 'form-control'
        self.fields['content'].widget.attrs['placeholder'] = '댓글을 남겨주세요!'

class Fun_imageForm(forms.ModelForm):
    class Meta:
        model = Fun_Image
        fields = ['fun_image']

        labels = {
            'fun_image': '엽사'
        }

class SearchForm(forms.Form): 
    word = forms.CharField(label='Search Word')
