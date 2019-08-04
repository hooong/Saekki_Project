"""saekki_pro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
import promise.views
from django.conf import settings
from django.conf.urls.static import static
import accounts.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('promise/', include('promise.urls')),
    path('', promise.views.home, name = 'home'),
    path('aboutus/', promise.views.aboutus, name = 'aboutus'),
    path('accounts/', include('accounts.urls')),
    
    # 카카오로그인
    path('kakao/<str:operation>', accounts.views.kakao, name='kakao'),
    path('oauth/', accounts.views.oauth, name='oauth'),
    path('logout/', accounts.views.kakao_logout, name='kakao_logout'),
    path('signout/', accounts.views.kakao_signout, name='kakao_signout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
