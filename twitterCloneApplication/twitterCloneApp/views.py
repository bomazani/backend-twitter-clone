from django.shortcuts import render, HttpResponseRedirect, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import reverse

from twitterCloneApp.models import TwitterUser, Tweet, Notification
from twitterCloneApp.forms import TweetForm, SignupForm, LoginForm

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

    context = {
        'data':items,
        'current_user':request.user.twitteruser,
        'tweets':allTweets,
        'numtweets':numtweets,
    }
    return render(request, 'home.html', context)

@login_required()
def profile_view(request, twitteruser_id):
    myuser = TwitterUser.objects.get(id=twitteruser_id)
    mytweets = Tweet.objects.filter(author=myuser)
    numtweets = len(mytweets)
    context = {
        'current_user':myuser,
        'tweets':mytweets,
        'myuser':myuser,
        'numtweets':numtweets
    }
    return render(request, 'profile.html', context)

def single_user_view(request, username):
    username=username
    users = TwitterUser.objects.all()
    tweets = Tweet.objects.all()
    selecteduser = users.filter(user__username=username)
    user_tweetz = tweets.filter(author__user__username=username)
    # user_tweets = tweets.filter(author=selecteduser)
    current_user = request.user
    context = {
        'selecteduser':selecteduser,
        'tweets':tweets,
        'users':users,
        'username':username,
        'current_user':current_user,
        'user_tweetz':user_tweetz,
    }
    return render(request, 'singleuser.html', context)

def single_tweet_view(request, tweet_id):
    this_id = tweet_id
    tweets = Tweet.objects.all()
    singleTweet = Tweet.objects.filter(id=tweet_id)
    myuser = TwitterUser.objects.filter()

    # current_user = request.user.twitteruser
    # mytweets = Tweet.objects.filter(author=current_user)
    # numtweets = len(mytweets)
    context = {
        'singleTweet':singleTweet,
        'tweets':tweets,
        'this_id':this_id

        # 'current_user':current_user,
        # 'mytweets':mytweets,
        # 'numtweets':numtweets,
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
    items = Notification.objects.filter(twitter_user=current_user)
    mytweets = Tweet.objects.filter(author=current_user.id)
    numtweets = len(mytweets)
    myrequest = request

    context = {
        'current_user':request.user.twitteruser,
        'numtweets':numtweets,
        'notifications': items,
        'mytweets': mytweets,
        'myrequest': myrequest,
    }
    return render(request, 'notification.html', context)

# def follow_view(request):
#     ''' obtained from djeets. May need to adjust names/variables. '''
#     userids = {}
#     for id in request.user.profile.follows.all():
#         userids.append(id)
#     userids.append(request.user.id)
#     followtweets = Tweet.objects.filter(user_id__in=userids)

#     return render(request, 'feed.html', {'followtweets':followtweets})
    # return render(request, 'displayFollowTweets.html', {'followtweets':followtweets})

# def follows(request, username):
#     ''' obtained from djeets. May need to adjust names/variables. '''
#     user = TwitterUser.objects.get(username=username)
#     tweeterprofiles = user.twitterprofile.follows.select_related('user').all()

#     return render(request, 'users.html', {'title': 'Follows', 'twitterprofiles': twitterprofiles})

# def followers(request, username):
#     ''' obtained from djeets. May need to adjust names/variables. '''
#     user = TwitterUser.objects.get(username=username)
#     tweeterprofiles = user.twitterprofile.followed_by.select_related('user').all()

#     return render(request, 'users.html', {'title': 'Followers', 'twitterprofiles': twitterprofiles})

@login_required
def follow_view(request, username):
    

@login_required
def add_follow(request, username):
    # current_user = request.user.twitteruser
    # user = TwitterUser.objects.get(username=username)
    # user = get_object_or_404(TwitterUser, username=user_name)
    # request.user.twitterprofile.follows.add(user.twitterprofile)
    to_follow = TwitterUser.objects.filter(username=username).first()
    html = 'sidebar.html'
    add_follow(request, username)
    return HttpResponseRedirect(reverse('sidebar', kwargs={'username': username}))

@login_required
def remove_follow(request, username):
    # current_user = request.user.twitteruser
    # user = TwitterUser.objects.get(username=username)
    # user = get_object_or_404(TwitterUser, username=user_name)
    # request.user.twitterprofile.follows.delete(user.twitterprofile)
    to_unfollow = TwitterUser.objects.filter(username=username).first()
    html = 'sidebar.html'
    add_follow(request, username)
    return HttpResponseRedirect(reverse('sidebar', kwargs={'username': username}))
