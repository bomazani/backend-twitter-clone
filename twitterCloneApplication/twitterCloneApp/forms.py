from django import forms
from twitterCloneApp.models import TwitterUser, Tweet, Notification

class SignupForm(forms.Form):
    username = forms.CharField(label=" Username.", max_length=50)
    email = forms.EmailField(label="Email", )
    password = forms.CharField(widget=forms.PasswordInput())

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())

class TweetForm(forms.Form):
    body = forms.CharField(label='Say what ya gotta say...', widget=forms.Textarea)
    author = forms.ModelChoiceField(label='Tweet Author', queryset=TwitterUser.objects.all())
    # time_tweeted = forms.???????