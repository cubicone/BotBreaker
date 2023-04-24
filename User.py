# Tumblr API User Functions
# The following is an organised, usable set of all functions which pertain to user actions (all of which require OAuth1)
# This is in service of the BotBreaker project
# Ver 1.0.0

import requests
from requests_oauthlib import OAuth1

class User:

    # constructor for User
    def __init__(self, uuid_, api_key_, api_secret_, oauth_key_, oauth_secret_):
        self.uuid = uuid_
        self.api_key = api_key_
        self.api_secret = api_secret_
        self.oauth_key = oauth_key_
        self.oauth_secret = oauth_secret_
        self.oauth = OAuth1(client_key=self.api_key,
                            client_secret=self.api_secret,
                            resource_owner_key=self.oauth_key,
                            resource_owner_secret=self.oauth_secret)

        # all requests start thus
        self.base_url = "https://api.tumblr.com/v2/user/"


    # user info 
    # requires `auth`
    # `auth` is system handled
    def userInfo(self):
        # build request
        request = self.base_url+"info"
        # return response
        return requests.get(request, auth=self.oauth)

    # user limits
    # requires `auth`
    # `auth` is system handled
    def userLimits(self):
        # build request
        request = self.base_url+"limits"
        # return response
        return requests.get(request, auth=self.oauth)

    # user dashboard
    # requires `auth`
    # `auth` is system handled
    # `type` defines the type of posts to return ("", "text", "photo", "quote", "link", "chat", "audio", "video", "answer") [""]    
    # `offset` defines the index to begin at in the complete blocked list [0]
    # `limit` defines the number of posts to pull from the index [20] {max 20}
    # `since_id` defines the timestamp before which to look for posts
    # `reblog_info` determines if extra reblog-type info is returned ["True"]
    # `notes_info` determines if extra notes-type info is returned ["True"]
    # `npf` return in npf format ["True"]
    def userDashboard(self, type="", limit=20, offset=0, since_id=0, reblog_info=True, notes_info=True, npf=True):
        # prepare json for request
        json = {"limit" : limit, 
                "offset" : offset, 
                "type" : type, 
                "since_id" : since_id, 
                "reblog_info" : reblog_info,
                "notes_info" : notes_info,
                "npf" : npf
            }

        # build request
        request = self.base_url+"dashboard"
        # return response
        return requests.get(request, json=json, auth=self.oauth)

    # user likes
    # requires `auth`
    # `auth` is system handled
    # `offset` defines the index to begin at in the complete blocked list [0]
    # `limit` defines the number of posts to pull from the index [20] {max 20}
    # `before` is the timestamp (in seconds) before which the system will look for data [-1]
    # `after` is the timestamp (in seconds) after which the system will look for data [-1]
    def userLikesList(self, limit=20, offset=0, before=0, after=0):
        request = self.base_url+"likes"

        # constructs data given in the correct order and then returns the response
        # hierarchy is thus: `before` -> `after` -> `offset`
        # `limit` can coexist with `before` or `after` or `offset`
        # but `before` and `after` and `offset` cannot coexist
        if not (before == -1):
            return requests.get(request, json={"limit" : limit, "before" : before}, auth=self.oauth)
        elif not (after == -1):
            return requests.get(request, json={"limit" : limit, "after" : after}, auth=self.oauth)
        elif not (offset == 0):
            if (offset > 1000):
                print("Offset exceeds 1000. Use before or after.")
                return ""

            return requests.get(request, json={"limit" : limit, "offset" : offset}, auth=self.oauth)
        else:
            return requests.get(request, json={"limit" : limit, "offset" : offset}, auth=self.oauth)

    # user following
    # requires `auth`
    # `auth` is system handled
    # `offset` defines the index to begin at in the complete blocked list [0]
    # `limit` defines the number of posts to pull from the index [20] {max 20}
    def userFollowingList(self, limit=20, offset=0):
        # build requests
        request = self.base_url+"following"
        # return response
        return requests.get(request, json={"limit" : limit, "offset" : offset}, auth=self.oauth)

    # follow
    # requires `auth`, and `url` or `email`
    # `auth` is system handled
    # `url` is the url of the blog to follow
    # `email` of the blog to follow provided its
    def follow(self, url, email=""):
        # build requests
        request = self.base_url+"follow"

        # declare json
        json = {}
        
        # decide if url or email should be used
        if (url == ""):
            json['email'] = email
        else:
            json['url'] = url

        # return responses
        return requests.post(request, json=json, auth=self.oauth)

    # unfollow
    # requires `auth`, and `url`
    # `auth` is system handled
    # `url` is the url of the blog to unfollow
    def unfollow(self, url):
        # build request
        request = self.base_url+"unfollow"

        # build json
        json = {"url" : url}

        # return the response
        return requests.post(request, json=json, auth=self.oauth)


    # like
    # requires `auth`, `post_id`, and `reblog_key`
    # `auth` is system handled
    # `post_id` is the id of the post to like
    # `reblog_key` is the reblog key of the post to like
    def like(self, post_id, reblog_key):
        # build request
        request = self.base_url+"like"
        # build json
        json = {"id" : post_id, "reblog_key" : reblog_key}
        # return response
        return requests.post(request, json=json , auth=self.oauth)

    # unlike
    # requires `auth`, `post_id`, and `reblog_key`
    # `auth` is system handled
    # `post_id` is the id of the post to unlike
    # `reblog_key` is the reblog key of the post to unlike
    def unlike(self, post_id, reblog_key):
        # build request
        request = self.base_url+"unlike"
        # build json
        json = {"id" : post_id, "reblog_key" : reblog_key}
        # return response
        return requests.post(request, json=json , auth=self.oauth)

    # get filtered tags
    # requires `auth`
    # `auth` is system handled
    def getFilteredTags(self):
        # build request
        request = self.base_url+"filtered_tags"
        # return response
        return requests.get(request, auth=self.oauth)

    # add tag filter
    # requires `auth`, and `filtered_tags`
    # `auth` is system handled
    # `filtered_tags` is the list of tags to add to the filter list
    def addTagFilter(self, filtered_tags):
        # build request
        request = self.base_url+"filtered_tags"
        # build json
        json = {"filtered_tags" : filtered_tags}
        # return response
        return requests.post(request, json=json, auth=self.oauth)

    # remove tag filter
    # requires `auth`, and `tag`
    # `auth` is system handled
    # `tag` is the tag you wish to delete from the tag list
    def removeTagFilter(self, tag):
        # build request
        request = self.base_url+"filtered_tags/"+str(tag)
        # returns the response
        return requests.delete(request, auth=self.oauth)
