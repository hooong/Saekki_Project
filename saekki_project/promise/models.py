from django.db import models
from django.contrib.auth.models import User
from saekki_pro import settings
from django.contrib.postgres.fields import ArrayField

# 약속게시물
class Promise(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    setting_date_time = models.CharField(max_length=200)
    pre_party = ArrayField(models.CharField(max_length=15),  default=list, null=True, blank=True)
    acpt_party = ArrayField(models.CharField(max_length=15),  default=list, null=True, blank=True)

    # 벌칙 관련
    # 벌칙 종류 (0:벌칙 없읍, 1: 벌금, 2: 엽사)
    what_betting = models.CharField(max_length=30, default='0', null=True, blank=True)
    # 벌금 기준 (0:기본, 1: 시간당, 2: 1회)
    per_or_one = models.CharField(max_length=30, default='0', null=True, blank=True)
    per_min_money = models.CharField(max_length=255, default='100', null=True, blank=True)
    setting_min = models.CharField(max_length=50, default='1', null=True, blank=True)
    onetime_panalty = models.CharField(max_length=50, default='0', null=True, blank=True)

    # 경도
    longitud = models.FloatField(null=True, blank=True, default=None)
    # 위도
    latitude = models.FloatField(null=True, blank=True, default=None)
    # 종료되었는지 여부
    end = models.PositiveSmallIntegerField(default=0)
    # 마감임박
    soon = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.title

# 약속게시물 내 댓글
class Promise_Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    promise = models.ForeignKey(Promise, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# 친구 model
class Friend(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    current_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owner', null=True, on_delete=models.CASCADE)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user = current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user = current_user
        )
        friend.users.remove(new_friend)

# 도착여부를 확인하기위한 모델
class Party_detail(models.Model):
    promise = models.ForeignKey(Promise, related_name='party_detail', null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

    # 벌금
    penalty = models.CharField(max_length=200, default='0', null=True, blank=True)

    # 수락여부
    acpt = models.PositiveSmallIntegerField(default=0)       # 1 : 수락 , 2 : 거절

    # 성공여부
    success_or_fail = models.PositiveSmallIntegerField(default=0)
    arrived_time = models.DateTimeField(null=True, blank=True, default=None)

# 엽사(배팅) 모델
class Fun_Image(models.Model):
    user = models.ForeignKey(Party_detail, related_name='fun', null=True, on_delete=models.CASCADE)
    # 엽사
    fun_image = models.ImageField(blank=True, null=True, upload_to="promise_fun_tmp")

# 친구신청 알림 모델
class Notification_friend(models.Model):
    send_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='firend_send_user', null=True, on_delete=models.CASCADE)
    receive_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='firend_receive_user', null=True, on_delete=models.CASCADE)

# 약속,댓글 알림 모델
class Notification_promise(models.Model):
    send_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='promise_send_user', null=True, on_delete=models.CASCADE)
    receive_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='promise_receive_user', null=True, on_delete=models.CASCADE)
    promise = models.ForeignKey(Promise, related_name='promise_noti', null=True, on_delete=models.CASCADE)
    com_or_pro = models.CharField(max_length=1, null=True)

class Notification_penalty(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='penalty_user', null=True, on_delete=models.CASCADE)
    promise = models.ForeignKey(Promise, related_name='penalty_promise', null=True, on_delete=models.CASCADE)
    penalty = models.CharField(max_length=200, default='0')
    final = models.CharField(max_length=5, default='0')

