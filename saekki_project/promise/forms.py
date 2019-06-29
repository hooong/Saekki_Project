from django import forms
from .models import Promise
from tempus_dominus.widgets import DateTimePicker

class PromiseForm(forms.ModelForm):

    class Meta:
        model = Promise
        fields = ['title', 'content', 'setting_date_time']
        widgets = {
            'setting_date_time': DateTimePicker(options={'defaultDate': '2019-05-31T00:00:00'},
            attrs={'input_toggle': True,}),
        }
        labels = {
            'title': '제목',
            'content': '약속내용',
            'setting_date_time': '약속 날짜/시간',
        }