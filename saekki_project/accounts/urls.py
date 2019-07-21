from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', include('django.contrib.auth.urls')),
    path('mypage/', views.mypage, name='mypage'),
    # path('logout/', views.logout name='logout'),
]