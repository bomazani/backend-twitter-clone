from django.shortcuts import render, HttpResponseRedirect, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import reverse
from copy import deepcopy

from twitterCloneApp.models import TwitterUser, Tweet, Notification
from twitterCloneApp.forms import TweetForm, SignupForm, LoginForm
from twitterCloneApp.helpers import add_follower, remove_follower


def signup_view(request):
    html = 'genericForm.html'
    form = None

    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username=data['username'],
                password=data['password'],
                email=data['email']
            )
            login(request, user)
            TwitterUser.objects.create(
                user=user,
            )
            return HttpResponseRedirect(reverse('home'))
    else:
        form = SignupForm()

    return render(request, html, {'form': form})


def login_view(request):
    html = 'login.html'
    form = None

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'],
                password=data['password']
            )
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', '/'))
    else:
        form = LoginForm()

    return render(request, html, {'form': form})


def logout_view(request):
    logout(request)

    return HttpResponseRedirect("/")


@login_required()
def home_view(request):
    items = TwitterUser.objects.all()
    allTweets = Tweet.objects.all()
    current_user = request.user.twitteruser
    mytweets = Tweet.objects.filter(author=current_user.id)
    numtweets = len(mytweets)
    # followed_authors = TwitterUser.objects.filter(follows=True)
    # followed_tweets = Tweet.objects.get(author=followed_authors)
    # followed_tweets = Tweet.objects.get(author in followed_authors)
    user = request.user
    user_name = request.user.username
    # mytweets = Tweet.objects.filter(author=myuser)
    numtweets = len(mytweets)
    current_follows = request.user.twitteruser.follows.all()
    numfollows = len(current_follows)
    # followed_tweets = Tweet.objects.get().filter(author=followed_authors)
    gathered_tweets = []
    # for auth in followed_authors:
        # gathered_tweets.append(Tweet.objects.get(author=auth))
    # for tweet in allTweets:
        # if (tweet.author.follows == True) or (tweet.author == current_user):
        # if (tweet in followed_tweets) or (tweet.author == current_user):
        # if (tweet.author == current_user):
        #     gathered_tweets.append(tweet)
    # for tweet in followed_tweets:
    #     gathered_tweets.append(tweet)
    for tweet in allTweets:
        # for auth in followed_authors:
        if tweet.author == current_user:
            gathered_tweets.append(tweet)
        for auth in current_follows:
            if tweet.author == auth and tweet.author != current_user:
                gathered_tweets.append(tweet)
    followed_tweets = []
    for tweet in allTweets:
        for auth in current_follows:
            if tweet.author == auth :
                followed_tweets.append(tweet)
    context = {
        'data':items,
        'current_user':request.user.twitteruser,
        'tweets':allTweets,
        'numtweets':numtweets,
        'numfollows': numfollows,
        'gathered_tweets': gathered_tweets,
        'followed_authors': current_follows,
        'followed_tweets': followed_tweets,
        'current_follows': current_follows,
    }

    return render(request, 'home.html', context)


def single_user_view(request, username):
    username=username
    user = request.user
    users = TwitterUser.objects.all()
    tweets = Tweet.objects.all()
    selecteduser = users.filter(user__username=username)
    user_tweetz = tweets.filter(author__user__username=username)
    # user_tweets = tweets.filter(author=selecteduser)
    current_user = request.user
    myuser = TwitterUser.objects.get(username=username)
    if user.is_authenticated:
        current_follows = request.user.twitteruser.follows.all()
        if myuser in current_follows:
            following = True
            not_following = False
        else:
            following = False
            not_following = True

        context = {
            'selecteduser':selecteduser,
            'tweets':tweets,
            'users':users,
            'username':username,
            # 'myuser': myuser,
            'current_user':current_user,
            # 'current_follows':current_follows,
            'user_tweetz':user_tweetz,
            'following': following,
            'not_following': not_following,
        }

        return render(request, 'singleuser.html', context)

    else:
        context = {
            'selecteduser':selecteduser,
            'tweets':tweets,
            'users':users,
            'username':username,
            # 'myuser': myuser,
            'current_user':current_user,
            # 'current_follows':current_follows,
            'user_tweetz':user_tweetz,
            # 'following': following,
            # 'not_following': not_following,

        }

    return render(request, 'singleuser.html', context)


def single_tweet_view(request, tweet_id):
    this_id = tweet_id
    tweets = Tweet.objects.all()
    singleTweet = Tweet.objects.filter(id=tweet_id)
    myuser = TwitterUser.objects.filter()

    context = {
        'singleTweet':singleTweet,
        'tweets':tweets,
        'this_id':this_id
    }

    return render(request, 'singleTweet.html', context)


@login_required()
def add_tweet(request):
    html = 'addTweet.html'
    form = None
    items = TwitterUser.objects.all()
    created_on = Tweet.tweetTime
    current_user = request.user.twitteruser
    mytweets = Tweet.objects.filter(author=current_user.id)
    numtweets = len(mytweets)

    context = {
        'data':items,
        'current_user':request.user.twitteruser,
        'created_on':created_on,
        'numtweets':numtweets
    }

    if request.method == "POST":
        form = TweetForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            # create an empty list for regex matches
            matches = []
            # call an unsaved instance of the tweet
            t = Tweet(
                body=data['body'],
                author=request.user.twitteruser,
            )
            # save the instance of the new tweet
            t.save()
            # call the 'create_notifications' function from the Tweet model
            t.create_notifications()
            return HttpResponseRedirect(reverse('home'), context)

    else:
        form = TweetForm()
    context.update({'form': form})

    return render(request, html, context)


@login_required
def notification_view(request):
    current_user = request.user.twitteruser
    items = Notification.objects.filter(twitter_user=current_user).filter(viewed=False)
    
    for i in items:
        i.viewed = True
        i.save()

    mytweets = Tweet.objects.filter(author=current_user.id)
    numtweets = len(mytweets)
    myrequest = request

    context = {
        'current_user':request.user.twitteruser,
        'numtweets':numtweets,
        'notifications': items,
        'mytweets': mytweets,
        'myrequest': myrequest,
        'items': items,
    }
    
    return render(request, 'notification.html', context)


@login_required()
def profile_view(request, twitteruser_id):
    user = request.user
    user_name = request.user.username
    myuser = TwitterUser.objects.get(id=twitteruser_id)
    mytweets = Tweet.objects.filter(author=myuser)
    numtweets = len(mytweets)

    current_follows = request.user.twitteruser.follows.all()
    numfollows = len(current_follows)

    if myuser in current_follows:
        following = True
        not_following = False

    else:
        following = False
        not_following = True

    if (str(user_name) == str(myuser)):
        match = True
    else:
        match = False

    data = {
        'current_user':myuser,
        'tweets':mytweets,
        'myuser':myuser,
        'numtweets':numtweets,
        'twitteruser_id':twitteruser_id,
        'user':user,
        'current_follows': current_follows,
        'following': following,
        'not_following': not_following,
        'match': match,
        'numfollows': numfollows
    }
   
    return render(request, 'profile.html', data)


@login_required
def add_follow(request, username):
    user = request.user
    username = username
    viewed_user = TwitterUser.objects.filter(username=username).first()
    html = 'profile.html'
    myuser = TwitterUser.objects.get(username=username)
    viewed_user_id = viewed_user.id
    twitteruserid = myuser.id

    add_follower(request, viewed_user)

    user = request.user
    user_name = request.user.username
    myuser = TwitterUser.objects.get(id=viewed_user_id)
    mytweets = Tweet.objects.filter(author=myuser)
    numtweets = len(mytweets)
    current_follows = request.user.twitteruser.follows.all()
    numfollows = len(current_follows)
    # twitteruser_id = 'xyz'

    if myuser in current_follows:
        following = True
        not_following = False

    else:
        following = False
        not_following = True

    if (str(user_name) == str(myuser)):
        match = True
    else:
        match = False

    context = {
        'current_user':myuser,
        'tweets':mytweets,
        'myuser':myuser,
        'numtweets':numtweets,
        # 'twitteruser_id':twitteruser_id,
        'user':user,
        'current_follows': current_follows,
        'following': following,
        'not_following': not_following,
        'match': match,
        'numfollows': numfollows,
        'username': username,
        'viewed_user': viewed_user,
        'viewed_user_id': viewed_user_id,
        'twitteruserid': twitteruserid,
    }

    return render(request, 'profile.html', context)


@login_required
def remove_follow(request, username):
    user = request.user
    username = username
    viewed_user = TwitterUser.objects.filter(username=username).first()
    html = 'profile.html'
    myuser = TwitterUser.objects.get(username=username)
    viewed_user_id = viewed_user.id
    twitteruserid = myuser.id

    remove_follower(request, viewed_user)

    user = request.user
    user_name = request.user.username
    myuser = TwitterUser.objects.get(id=viewed_user_id)
    mytweets = Tweet.objects.filter(author=myuser)
    numtweets = len(mytweets)
    current_follows = request.user.twitteruser.follows.all()
    numfollows = len(current_follows)
    # twitteruser_id = 'xyz'

    if myuser in current_follows:
        following = True
        not_following = False

    else:
        following = False
        not_following = True

    if (str(user_name) == str(myuser)):
        match = True
    else:
        match = False

    context = {
        'current_user': myuser,
        'tweets': mytweets,
        'myuser': myuser,
        'numtweets': numtweets,
        # 'twitteruser_id': twitteruser_id,
        'user': user,
        'current_follows': current_follows,
        'following': following,
        'not_following': not_following,
        'match': match,
        'numfollows': numfollows,
        'username': username,
        'viewed_user': viewed_user,
        'viewed_user_id': viewed_user_id,
        'twitteruserid': twitteruserid,
        'numfollows': numfollows,
    }

    return render(request, 'profile.html', context)


@login_required
def follow(request, username):
    user = request.user
    username = username
    viewed_user = TwitterUser.objects.filter(username=username).first()
    viewed_username = viewed_user.username
    html = 'singleuser.html'
    myuser = TwitterUser.objects.get(username=username)
    viewed_user_id = viewed_user.id
    twitteruserid = myuser.id

    add_follower(request, viewed_user)

    user = request.user
    user_name = request.user.username
    myuser = TwitterUser.objects.get(id=viewed_user_id)
    # viewed_user = TwitterUser.objects.filter(username=username).first()
    mytweets = Tweet.objects.filter(author=myuser)
    # tweets = Tweet.objects.filter(author=viewed_username)
    numtweets = len(mytweets)
    current_follows = request.user.twitteruser.follows.all()
    numfollows = len(current_follows)
    # twitteruser_id = 'xyz'

    if myuser in current_follows:
        following = True
        not_following = False

    else:
        following = False
        not_following = True

    if (str(user_name) == str(myuser)):
        match = True
    else:
        match = False

    context = {
        'current_user':myuser,
        'user_tweetz':mytweets,
        # 'tweets': tweets,
        'myuser':myuser,
        'numtweets':numtweets,
        # 'twitteruser_id':twitteruser_id,
        'user':user,
        'current_follows': current_follows,
        'following': following,
        'not_following': not_following,
        'match': match,
        'numfollows': numfollows,
        'username': username,
        'viewed_user': viewed_user,
        'viewed_user_id': viewed_user_id,
        'twitteruserid': twitteruserid,
    }

    return render(request, 'singleuser.html', context)


@login_required
def unfollow(request, username):
    user = request.user
    username = username
    viewed_user = TwitterUser.objects.filter(username=username).first()
    html = 'singleuser.html'
    myuser = TwitterUser.objects.get(username=username)
    viewed_user_id = viewed_user.id
    twitteruserid = myuser.id

    remove_follower(request, viewed_user)

    user = request.user
    user_name = request.user.username
    myuser = TwitterUser.objects.get(id=viewed_user_id)
    mytweets = Tweet.objects.filter(author=myuser)
    # tweets = Tweet.objects.filter(author=username)
    numtweets = len(mytweets)
    current_follows = request.user.twitteruser.follows.all()
    numfollows = len(current_follows)
    # twitteruser_id = 'xyz'

    if myuser in current_follows:
        following = True
        not_following = False

    else:
        following = False
        not_following = True

    if (str(user_name) == str(myuser)):
        match = True
    else:
        match = False

    context = {
        'current_user': myuser,
        'user_tweetz': mytweets,
        # 'tweets': tweets,
        'myuser': myuser,
        'numtweets': numtweets,
        # 'twitteruser_id': twitteruser_id,
        'user': user,
        'current_follows': current_follows,
        'following': following,
        'not_following': not_following,
        'match': match,
        'numfollows': numfollows,
        'username': username,
        'viewed_user': viewed_user,
        'viewed_user_id': viewed_user_id,
        'twitteruserid': twitteruserid,
        'numfollows': numfollows,
    }

    return render(request, 'singleuser.html', context)
