from django.db import models
from django.contrib.auth.models import User

# 약속게시물
class Promise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    setting_date_time = models.CharField(max_length=200)
    # TODO
    # 위치정보

    def __str__(self):
        return self.title

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

# 참가원 models
class Party(models.Model):
    users = models.ManyToManyField(User)
    current_promise = models.ForeignKey(Promise, related_name='owner_promise', null=True, on_delete=models.CASCADE)

    @classmethod
    def make_party(cls, current_promise, new_party):
        party, created = cls.objects.get_or_create(
            current_promise = current_promise
        )
        party.users.add(new_party)