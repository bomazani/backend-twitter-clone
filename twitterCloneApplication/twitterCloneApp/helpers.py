def add_follower(request, viewed_user):
    request.user.twitteruser.follows.add(viewed_user)

def remove_follower(request, viewed_user):
    request.user.twitteruser.follows.remove(viewed_user)
