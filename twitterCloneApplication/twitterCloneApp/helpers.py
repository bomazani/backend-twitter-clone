def add_follow(request, twitteruser):
    request.user.follow.add(twitteruser)

def remove_follow(request, twitteruser):
    request.user.follow.remove(twitteruser)