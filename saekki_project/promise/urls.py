from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.new, name='new'),
    path('detail/<int:pk>', views.detail, name='detail'),
    url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_friend, name='change_friend')
]