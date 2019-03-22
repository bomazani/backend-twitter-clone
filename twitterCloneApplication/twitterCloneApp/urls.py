"""twitterCloneApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from twitterCloneApp import views
from django.conf import settings
from django.urls import include, path
from twitterCloneApp.models import *
from twitterCloneApp.views import home_view, login_view, signup_view, logout_view, tweet_view, profile_view, notification_view, add_tweet

admin.site.register(TwitterUser)
admin.site.register(Tweet)
admin.site.register(Notification)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('tweet/<int:tweet_id>', views.tweet_view, name='tweet'),
    path('add_tweet/', views.add_tweet, name='add_tweet'),
    path('notification/', views.notification_view, name='notification'),
    path('profile/<int:twitteruser_id>', views.profile_view, name='profile'),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
