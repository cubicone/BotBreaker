# Tumblr API Blog Functions
# The following is an organised, usable set of all functions which pertain to Blog actions (all of which require OAuth1)
# This is in service of the BotBreaker project
# Ver 1.0.1

# import required libraries
import requests
from requests_oauthlib import OAuth1


class Blog2:
    # constructor for Blog
    # takes security object
    def __init__(self, security_):
        # extract all variables from the security object
        (
            self.uuid,
            self.api_key,
            self.api_secret,
            self.oauth_key,
            self.oauth_secret,
        ) = security_.getDetails()

        # use the extracted variables to create an OAuth1 object
        self.oauth = OAuth1(
            client_key=self.oauth_key,
            client_secret=self.oauth_secret,
            resource_owner_key=self.api_key,
            resource_owner_secret=self.api_secret,
        )

        # the base of all requests starts thus
        self.base_url = "https://api.tumblr.com/v2/blog/"

    # info
    # returns all info associated with a target blog
    # requires `target_blog` and can take `fields`
    # `target_blog` [String / UUID] is the id of the blog to pull info from
    # `fields` {Array of Strings} are the fields to pull exclusively if specified
    def info(self, target_blog, fields=[]):
        # if exclusive fields is not empty
        # parse the data into a string
        if not (fields == []):
            fields_final = ""

            # compile the fields to a HTTP friendly format - comma seperation
            for field in fields:
                fields_final = fields_final + field + ","

            # cut the final comma off the end
            fields_final = fields_final[:-1]

            # complie the request with exclusive fields
            request = f"{self.base_url}{target_blog}/info?api_key={self.api_key}&fields[blogs]={fields_final},?is_following_you,?duration_blog_following_you,?duration_following_blog,?timezone,?timezone_offset"
        else:
            # compile the request without completed fields
            request = f"{self.base_url}{target_blog}/info?api_key={self.api_key}"

        # send the request and return the response
        return requests.get(request, auth=self.oauth)

    # avatar
    # returns avatar specific data
    # requires `target_blog` and can take `size`
    # `target_blog` [String / UUID] specifies the id of the blog to pull avatar data from
    # `size` {64, 128, 256} is the width and height you want the square image to be [64]
    def avatar(self, target_blog, size=64):
        # build the request with the appropriate variables
        request = f"{self.base_url}{target_blog}/avatar/{str(size)}"
        # send the request and return the response
        return requests.get(request, auth=self.oauth)

    # blocked list
    # returns blocked list sample from specified index
    # requires `target_blog` and can take `offset` and `limit`
    # `target_blog` [String / UUID] specifies the id of the blog to pull blocked list data from
    # `offset` {Integer} specifies the index to begin pulling from in the master blocked list [0]
    # `limit` {Integer} specifies the number of posts to pull after beginning from the offset [20] {MAX 20}
    def blockedList(self, target_blog, offset=0, limit=20):
        # build the request with the appropriate variables
        request = f"{self.base_url}{target_blog}/blocks"
        # build json
        json = {"offset": offset, "limit": limit}
        # send the request and return the response
        return requests.get(request, params=json, auth=self.oauth)

    # block
    # posts block command to target blog from control blog
    # requires `control_blog` and `target_blog`
    # `control_blog` [String / UUID] specifies the id of the blog to block from
    # `target_blog` [String / UUID] specifies the id of the blog to block
    def block(self, control_blog, target_blog):
        # build the request with the appropriate variables
        request = f"{self.base_url}{control_blog}/blocks"
        # build json
        json = {"blocked_tumblelog": target_blog}
        # send the request and return the response
        return requests.post(request, params=json, auth=self.oauth)

    # bulk block
    # posts block command to a list of blogs in a single command
    # requires `control_blog` and `target_blogs`
    # `control_blog` [String / UUID] specifies the id of the blog to block from
    # `target_blogs` [Array of Strings / UUIDs] specifies a list of blog ids to block
    def bulkBlock(self, control_blog, target_blogs):
        # parse the target blogs input
        for blog in target_blogs:
            target_blogs_final = target_blogs_final + str(blog) + ","

        # cut the final comma off the end
        target_blogs_final = target_blogs_final[:-1]

        # build the request with the appropriate variables
        request = f"{self.base_url}{control_blog}/blocks/bulk"
        # build json
        json = {"blocked_tumblelogs": target_blogs_final}
        # send the request and return the response
        return requests.post(request, params=json, auth=self.oauth)

    # unblock
    # posts unblock command to the target blog
    # requires `control_blog` and `target_blog`
    # `control_blog` [String / UUID] specifies the id of the blog to unblock from
    # `target_blog` [String / UUID] specifies the id of the id to unblock
    def unblock(self, control_blog, target_blog):
        # build the request with the appropriate variables
        request = f"{self.base_url}{control_blog}/blocks"
        # build json
        json = {"blocked_tumblelog": target_blog}
        # send the request and return the response
        return requests.delete(request, params=json, auth=self.oauth)

    # likes list
    # returns a likes list sample from specified index
    # requires `target_blog` and can take `offset`, `limit`, `before`, and `after`
    # `target_blog` [String / UUID] specifies the id of the blog to pull likes from
    # `offset` {Integer} defines the index to begin at in the complete blocked list [0]
    # `limit` {Integer} defines the number of posts to pull from the index [20] {MAX 20}
    # `before` {Integer} defines the timestamp (in seconds) before which the system will look for data [-1]
    # `after` {Integer} defines the timestamp (in seconds) after which the system will look for data [-1]
    def likesList(self, target_blog, offset=0, limit=20, before="", after=""):
        # build the request with the appropriate variables
        request = f"{self.base_url}{target_blog}/likes?api_key={self.api_key}"

        # constructs data given in the correct order and then returns the response
        # hierarchy is thus: `before` -> `after` -> `offset`
        # `limit` can coexist with `before` or `after` or `offset`
        # but `before` and `after` and `offset` cannot coexist
        json = {"limit": limit}
        if not (before == ""):
            json["before"] = before
        elif not (after == ""):
            json["after"] = after
        else:
            json["offset"] = offset

        # send the request and return the response
        return requests.get(request, params=json, auth=self.oauth)

    # following list
    # returns a following list sample from specified index
    # `target_blog` [String / UUID] specifies the if of the blog to pull following list data from
    # `offset` {Integer} defines the index to begin at in the complete following list [0]
    # `limit` {Integer} defines the number of following to pull from the index [20] {max 20}
    def followingList(self, target_blog, offset=0, limit=20):
        # build the request with the appropriate variables
        request = f"{self.base_url}{target_blog}/following"
        # build json
        json = {"limit": limit, "offset": offset}
        # send the request and return the response
        return requests.get(request, params=json, auth=self.oauth)

    # followers list
    # returns a followers list sample from specified index
    # `target_blog` [String / UUID] specifies the id of the blog to pull followers list data from
    # `offset` [Integer] defines the index to begin at in the complete follower list [0]
    # `limit` [Integer] defines the number of followers to pull from the index [20] {max 20}
    def followersList(self, target_blog, offset=0, limit=20):
        # build the request with the appropriate variables
        request = f"{self.base_url}{target_blog}/followers"
        # build json
        json = {"limit": limit, "offset": offset}
        # send the request and return the response
        return requests.get(request, params=json, auth=self.oauth)

    # followed by
    # returns the followed by list
    # `target_blog` [String / UUID] specifies the id of the blog to pull followed by data from
    # `offset` [Integer] defines the index to begin at in the complete follower list [0]
    # `limit` [Integer] defines the number of followers to pull from the index [20] {max 20}
    def followedBy(self, control_blog, target_blog):
        # build the request with the appropriate variables
        request = f"{self.base_url}{control_blog}/followed_by?query={target_blog}"
        # send the request and return the response
        return requests.get(request, auth=self.oauth)

    # posts list
    # returns a posts list sample from specified index
    # requires `target_blog`and can take `type`, `specific_post_id`, `tags`, `offset`, `limit`, `reblog_info`, `notes_info`, `filter`, `before`, and `npf`
    # `target_blog` [String / UUID] specfies the if od the blog being pulled from
    # `type` {String} specifies the type of posts ('', 'text', 'quote', 'link', 'answer', 'video', 'audio' 'photo', 'chat') to return [""]
    # `specific_post_id` {String} specifies one specific post with a certain post id [""]
    # `tags` {Array} specifies that all posts should contain the selected tag(s) [[]]
    # `offset` {Integer} defines the index to begin at in the complete posts list [0]
    # `limit` {Integer} defines the number of posts to pull from the index [20] {max 20}
    # `reblog_info` {Boolean} determines if reblog info should be included in the response [True]
    # `notes_info` {Boolean} determines if notes info should be included in the response [True]
    # `filter` {String} specifies the HTML format [""]
    # `before` {Integer} is the timestamp (in seconds) before which the system will look for data [""]
    # `npf` {Boolean} determines whether the response should be in NPF format or not [False]
    def postsList(
        self,
        target_blog,
        type="",
        specific_post_id="",
        tags=[],
        offset=0,
        limit=20,
        reblog_info=True,
        notes_info=True,
        filter="",
        before="",
        npf=True,
    ):
        # begin request construction
        request = f"{self.base_url}{target_blog}/posts"

        # add type if not default [""]
        if not (type == ""):
            request += f"/{type}"

        # add api key
        request += f"?api_key={self.api_key}"

        # tag preperation
        tag_string = "?tag"

        # can tags be treated as a raw string?
        if not (tags == []):
            if len(tags) > 1:
                i = 0
                # properly format the query and heirarchy of tags
                for tag in tags:
                    tag_string = tag_string + "[" + i + "]=" + tag + "&"
                    i += 1
                tag_string = tag_string[:-1]
            else:
                tag_string = tag_string + "=" + str(tags[0])

            request += tag_string

        # determine which params to include
        json = {
            "limit": limit,
            "offset": offset,
            "reblog_info": reblog_info,
            "notes_info": notes_info,
            "npf": npf,
        }

        if not (specific_post_id == ""):
            json["specific_post_id"] = specific_post_id

        if not (filter == ""):
            json["filter"] = filter

        if not (before == ""):
            json["before"] = before

        # return the response
        return requests.get(request, params=json, auth=self.oauth)
