from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('mypage/', views.mypage, name='mypage'),
    path('mypage_mod/', views.mypage_modify, name='mypage_mod'),
    path('mypage_mod_conf/', views.mypage_mod_conf, name='mypage_mod_conf'),
]