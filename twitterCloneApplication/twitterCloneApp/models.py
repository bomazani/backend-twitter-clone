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
        TwitterUser,
        on_delete=models.CASCADE
    )
    body = models.TextField(null=True, blank=True)
    tweetTime = timezone.now()

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('username',)

class Notification(models.Model):
    ''' title and page below were added as dummy fields '''
    title = models.CharField(max_length=124, default='Filler Text')
    description = models.CharField(max_length=124, null=True, blank=True)
    tweets = models.ManyToManyField(Tweet)
    twitter_users = models.ManyToManyField(TwitterUser)

    def __str__(self):
        return self.tweets

    class Meta:
        ordering = ('title', )
 
