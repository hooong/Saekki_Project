from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', include('django.contrib.auth.urls')),
    path('mypage/', views.mypage, name='mypage'),
    # path('logout/', views.logout name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)