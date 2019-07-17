from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views
from .broker import schedule

urlpatterns = [
    path('new/', views.new, name='new'),
    path('detail/<int:pk>', views.detail, name='detail'),
    path('comment/<int:promise_id>', views.new_comment, name='new_comment'),
    path('arrived/<int:promise_id>', views.arrived, name='arrived'),
    path('promise_del/<int:promise_id>', views.pro_del, name='pro_del'),
    path('comment_del/<int:promise_id>/<int:comment_id>', views.com_del, name='com_del'),
    url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_friend, name='change_friend')
]

# 스케쥴러 작동
schedule()