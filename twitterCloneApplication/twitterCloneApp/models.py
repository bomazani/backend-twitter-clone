from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

import re

class TwitterUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    username = models.CharField(max_length=124)
    follows = models.ManyToManyField("self", related_name='followed_by', symmetrical=False)

    def __str__(self):
        return self.user.username

class Notification(models.Model):
    tweet = models.ForeignKey(
        'Tweet',
        on_delete=models.CASCADE, null=True
    )

    twitter_user = models.ForeignKey(
        TwitterUser,
        on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        return self.tweet.author.user.username 

class Tweet(models.Model):
    author = models.ForeignKey(
        TwitterUser,
        on_delete=models.CASCADE
    )
    body = models.CharField(max_length=140, default='No message.')
    tweetTime = models.DateTimeField(auto_now=True)


    def create_notifications(self):
        text = self.body
        foundmatches = []
        matches = re.findall(r'@([a-zA-Z0-9_]+)', text)
        for match in matches:
            maybeuser = TwitterUser.objects.filter(user__username=match).first()
            if maybeuser is not None:
                Notification.objects.create(
                    tweet=self,
                    twitter_user=maybeuser
                )
                
    def __str__(self):
        return self.author.user.username

    class Meta:
        ordering = ('-tweetTime',)

