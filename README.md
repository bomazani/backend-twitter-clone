# backend-twitter-clone
Twitter clone created with Django.

- The following items must be met to meet the assignment requirements.

1) Users can access specific tweets by URL without being logged in:
    /singleTweet/<tweet_id>

2) Users can access specific users by URL without being logged in:
    /user/<username>
    
3) Users cannot access '/' without being logged in.

4) Users can sign up on their own.

5) Users get redirected to /login/ when attempting to load the homepage without being logged in.

6) Users have a page that they can write a 140 character tweet on.

7) After writing a tweet, that tweet appears (after a page refresh) for all accounts that follow the user (including the user).

8) Users can follow other users.

9) Users can unfollow other users.

10) Every tweet has a link to the author's profile page and a direct link to that specific tweet.

11) If a user mentions another through the @ syntax, that user receives a notification (after page refresh).

12) viewing notifications makes new notifications go away.

13) The user profile section has a count of how many tweets that user has written.

14) The user profile section has a count of how many accounts that user is following.

15) There is a working button that sends the logged-in user to their profile.

16) No logic contained in models, forms, or urls files

17) Uses only three custom models: TwitterUser (a one-to-one relationship with the Auth User), Tweet, and Notification.
