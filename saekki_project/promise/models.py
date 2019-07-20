from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# 약속게시물
class Promise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    setting_date_time = models.CharField(max_length=200)
    party = ArrayField(models.CharField(max_length=15),  default=list, null=True, blank=True)
    # 경도
    longitud = models.FloatField(null=True, blank=True, default=None)
    # 위도
    latitude = models.FloatField(null=True, blank=True, default=None)
    # 종료되었는지 여부
    end = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.title

# 약속게시물 내 댓글
class Promise_Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    promise = models.ForeignKey(Promise, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# 친구 model
class Friend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='owner', null=True, on_delete=models.CASCADE)

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
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    # 성공여부
    success_or_fail = models.PositiveSmallIntegerField(default=0)
    arrived_time = models.DateTimeField(null=True, blank=True, default=None)


# 친구신청 알림 모델
class Notification_friend(models.Model):
    send_user = models.ForeignKey(User, related_name='firend_send_user', null=True, on_delete=models.CASCADE)
    receive_user = models.ForeignKey(User, related_name='firend_receive_user', null=True, on_delete=models.CASCADE)