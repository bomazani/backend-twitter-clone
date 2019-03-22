from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class TwitterUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    username = models.CharField(max_length=124)
    follows = models.ManyToManyField("self", related_name='followed_by', symmetrical=False)

    def __str__(self):
        return self.user.username

class Tweet(models.Model):
    author = models.ForeignKey(
        TwitterUser,
        on_delete=models.CASCADE
    )
    body = models.CharField(max_length=140, default='No message.')
    tweetTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.author.user.username

    class Meta:
        ordering = ('-tweetTime',)

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
 
