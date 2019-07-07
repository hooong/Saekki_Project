from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views
from .broker import schedule

urlpatterns = [
    path('new/', views.new, name='new'),
    path('detail/<int:pk>', views.detail, name='detail'),
    path('arrived/<int:promise_id>', views.arrived, name='arrived'),
    url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_friend, name='change_friend')
]

schedule()