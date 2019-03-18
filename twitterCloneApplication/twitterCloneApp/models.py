from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class TwitterUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    username = models.CharField(max_length=124)
    followed_users = models.ManyToManyField("self", symmetrical=False)

    def __str__(self):
        return self.user.username


class Tweet(models.Model):
    username = models.ForeignKey(
        TwitterUser.username,
        on_delete=models.CASCADE
    )
    body = models.TextField(null=True, blank=True)
    date_time = timezone.now()
    # recipient = 

def Notification(models.Model):
    pass
