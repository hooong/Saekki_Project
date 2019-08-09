from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views
from .broker import schedule
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('new/', views.new, name='new'),
    path('detail/<int:pk>', views.detail, name='detail'),
    path('comment/<int:promise_id>', views.new_comment, name='new_comment'),
    path('arrived/<int:promise_id>', views.arrived, name='arrived'),
    path('promise_del/<int:promise_id>', views.pro_del, name='pro_del'),
    path('comment_del/<int:promise_id>/<int:comment_id>', views.com_del, name='com_del'),
    path('addfriend/<int:pk>', views.add_friend, name='add_friend'),
    path('changefriend/<str:operation>/<int:pk>', views.change_friend, name='change_friend'),
    path('noti_promise/<str:operation>/<int:pk>', views.noti_promise_button, name='noti_promise_button'),
    path('search/', views.search, name='search'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('promise_acpt/<str:operation>/<str:promise_id>',views.acpt, name='promise_acpt'),
    path('fun_image/<int:promise_id>',views.fun_image,name='fun_image'),
    path('wanted/',views.wanted, name='wanted'),
    path('howtouse/', views.howtouse, name='howtouse'),
]
# 스케쥴러 작동
schedule()
