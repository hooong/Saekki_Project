from django import forms
from .models import Promise
from tempus_dominus.widgets import DateTimePicker
from django.utils import timezone

class PromiseForm(forms.ModelForm):

    class Meta:
        model = Promise
        fields = ['title', 'content', 'setting_date_time']

        time = str(timezone.now())
        time = time.replace(' ','T')
        time = time[:19]

        widgets = {
            'setting_date_time': DateTimePicker(options={'defaultDate': time },
            attrs={'input_toggle': True,}),
        }
        labels = {
            'title': '제목',
            'content': '약속내용',
            'setting_date_time': '약속 날짜/시간',
        }

