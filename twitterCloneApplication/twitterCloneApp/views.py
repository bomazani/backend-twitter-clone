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
    html = 'generic_form.html'
    form = None

    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username=data['username'],
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
    html = 'generic_form.html'
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
    return render(request, 'home.html', {'data':items})

@login_required()
def profile_view(request):
# def profile_view(request, user_id):
    items = get_object_or_404(TwitterUser)
    # items = get_object_or_404(TwitterUser, id=user_id)
    return render(request, 'profile.html', {'data':items})

@login_required()
def tweet_view(request):
    items = get_object_or_404(Tweet)
# def tweet_view(request, tweet_id):
#     items = get_object_or_404(TwitterUser, id=tweet_id)
    return render(request, 'tweet.html', {'data':items})

@login_required
def notification_view(request):
    items = get_object_or_404(Tweet)
    # return render(request, 'notification.html', {'data':items})
    # return render(request, 'notification.html', {'data': items})
    # return HttpResponseRedirect(request.GET.get('next', '/'))
    html = 'generic_form.html'
    form = None
    return render(request, html, {'form': form})



