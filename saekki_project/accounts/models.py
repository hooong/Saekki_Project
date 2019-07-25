from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True, upload_to='images/')
    state_msg = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user.username