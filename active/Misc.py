# Tumblr API Misc Functions
# The following is an organised, usable set of all functions which pertain to miscellaneous actions.
# This is in service of the BotBreaker project
# Ver 1.0.0

import requests
from requests_oauthlib import OAuth1

class Misc:

    # contructors for Misc
    def __init__(self, uuid="", api_key="", api_secret="", oauth_key="", oauth_secret=""):

        self.uuid = uuid
        self.api_key = api_key
        self.api_secret = api_secret
        self.oauth_key = oauth_key
        self.oauth_secret = oauth_secret
        self.oauth = OAuth1(client_key=self.api_key,
                            client_secret=self.api_secret,
                            resource_owner_key=self.oauth_key,
                            resource_owner_secret=self.oauth_secret)

        # all requests start thus
        self.base_url = "https://api.tumblr.com/v2/"

    # tagged
    # requires `auth` or `api_key`, and `tag`
    # `auth` is system handled
    # `api_key` is system handled
    # `tag` is the target tag that you want to pull info from
    # `before` determines the timestamp before which the posts should be pulled [""]
    # `limit` is the number of posts to return per response if more than this number is found (0-20) [20]
    # `filter` specifies the return format
    def tagged(self, tag="", before="", limit=20, filter=""):

        # builds base url
        request = self.base_url+"tagged?api_key="+self.api_key+"&tag="+tag

        # adds json
        json = {"limit" : limit,
                "filter" : filter}

        if not (before == ""):
            json["before"] = before

        # returns response
        return requests.get(request, params=json, auth=self.oauth)
