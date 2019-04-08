# backend-twitter-clone
Twitter clone created with Django

To read a single tweet without logging in: *working*
    /singletweet/<tweet_id>

To view a user without logging in: ** not working **
    /profile/<twitteruser_id>

user can follow other users *working*

user can unfollow other users *working*

viewing notifications makes new notifications go away ** not working **
    - How to change view attribute from False to True? 
    - Can I do it in my 'notification.html' template?

user profile has count of how many accounts that user is following ** not working on Home or Notifications pages. Currently only displays count for user on Profile page, not each specific user. **

** home page displays ALL tweets.

** Where do followed tweets display?

** I have created 3 html templates: all tweets, active user tweets, follower's tweets.
    - need to build those out, so they can be used to control what tweets are being displayed where.