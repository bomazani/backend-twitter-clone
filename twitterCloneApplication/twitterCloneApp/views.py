from django.shortcuts import render, HttpResponseRedirect
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

@login_required()
def tweet_view(request, twitteruser_id):
    tweets = Tweet.objects.all()
    myuser = TwitterUser.objects.get(id=twitteruser_id)
    mytweets = Tweet.objects.filter(author=myuser)
    numtweets = len(mytweets)
    context = {
        'current_user':myuser,
        'tweets':mytweets,
        'myuser':myuser,
        'numtweets':numtweets
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

            Tweet.objects.create(
                body=data['body'],
                author=request.user.twitteruser,
            )
            return HttpResponseRedirect(reverse('home'), context)

    else:
        form = TweetForm()
    context.update({'form': form})
    return render(request, html, context)

@login_required
def notification_view(request):
    items = Notification.objects.all()
    current_user = request.user.twitteruser
    mytweets = Tweet.objects.filter(author=current_user.id)
    numtweets = len(mytweets)

    context = {
        'data':items,
        'current_user':request.user.twitteruser,
        'numtweets':numtweets
    }
    return render(request, 'notification.html', context)



