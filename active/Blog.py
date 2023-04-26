# Tumblr API Blog Functions
# The following is an organised, usable set of all functions which pertain to Blog actions (all of which require OAuth1)
# This is in service of the BotBreaker project
# Ver 1.0.0

import requests
from requests_oauthlib import OAuth1
import random

class Blog:

    # constructors for Blog
    # first time
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
        self.base_url = "https://api.tumblr.com/v2/blog/"


    # info
    # requires `target_blog`, `api_key`, and `auth`
    # `target_blog` is the id of the blog to pull info data from
    # `api_key` is system handled
    # `auth` is system handled
    # `fields` limits the data returned to the specified attributes along with some extra data [[]]
    def info(self, target_blog, fields=[]):
        # defines fields processed string to be HTTPS ready
        fields_final = ""

        # configure fields_final
        if not (fields == []):
            # can it be treated as a raw string rather than a list?
            if (len(fields) > 1):
                for field in fields:
                    fields_final = fields_final + field + ","
            else:
                fields_final = fields[0] + ","

            request = self.base_url+target_blog+"/info?api_key="+self.api_key+"&fields[blogs]="+fields_final+"?is_following_you,?duration_blog_following_you,?duration_following_blog,?timezone,?timezone_offset"
        else:
            request = self.base_url+target_blog+"/info?api_key="+self.api_key
            
        # return the response
        return requests.get(request, auth=self.oauth)

    # avatar
    # requires `target_blog`, `auth`, and `size`
    # `target_blog` specifies the id of the blog to pull avatar data from 
    # `auth` is system handled
    # `size` is the width and height you want the square image to be [64]
    def avatar(self, target_blog, size=64):
        # build the request with the appropriate variables
        request = self.base_url+target_blog+"/avatar/"+str(size)
        # return the response
        return requests.get(request, auth=self.oauth)

    # blockedList
    # requires `target_blog`, and `auth`
    # `target_blog` specifies the id of the blog to pull blocked list data from
    # ` auth` is system handled
    # `offset` defines the index to begin at in the complete blocked list [0]
    # `limit` defines the number of posts to pull from the index [20] {max 20}
    def blockedList(self, target_blog, offset=0, limit=20):
        # build the request with the appropriate variables
        request = self.base_url+target_blog+"/blocks"
        # build json
        json = {"offset" : offset,
                "limit" : limit}
        # return the response
        return requests.get(request, params=json, auth=self.oauth)

    # block
    # requires `target_blog`, `control_blog`, and `auth`
    # `target_blog` specifies the id of the blog to block
    # `control_blog` specifies the id of the blog to block from
    # `auth` is system handled
    def block(self, control_blog, target_blog):
        # build the request with the appropriate variables
        request = self.base_url+control_blog+"/blocks"
        # build json
        json = {"blocked_tumblelog" : target_blog}
        # return the response
        return requests.post(request, params=json, auth=self.oauth)

    # bulkBlock
    # requires `target_blogs`, `control_blog`, and `auth`
    # `target_blogs` specifies the list of ids of blogs to block
    # `control_blog` specifies the id of the blog to block from
    # `auth` is system handled
    def bulkBlock(self, control_blog, target_blogs):
        # declare final processed blogs string
        target_blogs_final = ""

        # process the target blogs input
        for blog in target_blogs:
            target_blogs_final = target_blogs_final + str(blog) + ","
        target_blogs_final = target_blogs_final[:-1]

        # build the request with the appropriate variables
        request = self.base_url+control_blog+"/blocks/bulk"
        # build json
        json = {"blocked_tumblelogs" : target_blogs_final}
        # return the response
        return requests.post(request, params=json, auth=self.oauth)

    # unblock
    # requires `control_blog`, `target_blog`, and `auth`
    # `target_blog` specifies the id of the blog to unblock
    # `control_blog` specifies the id of the blog to unblock from
    # `auth` is system handled
    def unblock(self, control_blog, target_blog):
        # build the request with the appropriate variables
        request = self.base_url+control_blog+"/blocks"
        # build json
        json = {"blocked_tumblelog" : target_blog}
        # return the response
        return requests.delete(request, params=json, auth=self.oauth)

    # likes
    # requires `target_blog`, `api_key`, `auth`
    # `target_blog` specifies the id of the blog to pull likes data from
    # `api_key` is system handled
    # `auth` is system handled
    # `offset` defines the index to begin at in the complete blocked list [0]
    # `limit` defines the number of posts to pull from the index [20] {max 20}
    # `before` is the timestamp (in seconds) before which the system will look for data [-1]
    # `after` is the timestamp (in seconds) after which the system will look for data [-1]
    def likesList(self, target_blog, offset=0, limit=20, before="", after=""):
        # build the request with the appropriate variables
        request = self.base_url+target_blog+"/likes?api_key="+self.api_key
        
        # constructs data given in the correct order and then returns the response
        # hierarchy is thus: `before` -> `after` -> `offset`
        # `limit` can coexist with `before` or `after` or `offset`
        # but `before` and `after` and `offset` cannot coexist
        json = {"limit" : limit}
        if not (before == ""):
            json['before'] = before
        elif not (after == ""):
            json['after'] = after
        else:
            json['offset'] = offset

        return requests.get(request, params=json, auth=self.oauth)
        
    # following
    # requires `target_blog`, and `auth`
    # `target_blog` specifies the id of the blog to pull following list data from
    # `auth` is system handled
    # `offset` defines the index to begin at in the complete following list [0]
    # `limit` defines the number of following to pull from the index [20] {max 20}
    def followingList(self, target_blog, offset=0, limit=20):
        # build the request with the appropriate variables
        request = self.base_url+target_blog+"/following"
        # build json
        json = {"limit" : limit, 
                "offset" : offset}
        # return the response
        return requests.get(request, params=json, auth=self.oauth)

    # followers
    # requires `target_blog`, and `auth`
    # `target_blog` specifies the id of the blog to pull follower list data from
    # `auth` is system handled
    # `offset` defines the index to begin at in the complete follower list [0]
    # `limit` defines the number of followers to pull from the index [20] {max 20}
    def followersList(self, target_blog, offset=0, limit=20):
        # build the request with the appropriate variables
        request = self.base_url+target_blog+"/followers"
        # build json
        json = {"limit" : limit, 
                "offset" : offset}
        # return the response
        return requests.get(request, params=json, auth=self.oauth)

    # followedBy
    # requires `control_blog`, `target_blog`, and `auth`
    # `control_blog` specifies the id of the blog you are checking is being followed by `target_blog`
    # `target_blog` specifies the id of the blog you are checking is following `control_blog`
    # `auth` is system handled
    def followedBy(self, control_blog, target_blog):
        # build the request with the appropriate variables
        request = self.base_url+control_blog+"/followed_by?query="+target_blog
        # return the response
        return requests.get(request, auth=self.oauth)

    # posts list
    # requires `target_blog`, `api_key` and `auth`
    # `target_blog` specfies the id of the blog you are pulling the posts data from
    # `api_key` is system handled
    # `auth` is system handled
    # `type` specifies the type of posts ('', 'text', 'quote', 'link', 'answer', 'video', 'audio' 'photo', 'chat') to return [""]
    # `specific_post_id` specifies one specific post with a certain post id [""]
    # `tags` specifies that all posts should contain the selected tag(s) [[]]
    # `offset` defines the index to begin at in the complete posts list [0]
    # `limit` defines the number of posts to pull from the index [20] {max 20}
    # `reblog_info` determines if reblog info should be included in the response [True]
    # `notes_info` determines if notes info should be included in the response [True]
    # `filter` specifies the HTML format [""]
    # `before` is the timestamp (in seconds) before which the system will look for data [""]
    # `npf` determines whether the response should be in NPF format or not [False]
    def postsList(self, target_blog, type="", specific_post_id="", tags=[], offset=0, limit=20, reblog_info=True, notes_info=True, filter="", before="", npf=True):
        # begin request construction
        request = self.base_url+target_blog+"/posts"

        # add type if not default [""]
        if not (type == ""):
            request += "/"+type

        # add api key
        request = request+"?api_key="+self.api_key

        # tag preperation
        tag_string = "?tag"

        # can tags be treated as a raw string?
        if not (tags == []):
            if (len(tags) > 1):
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
        json = {"limit" : limit,
                "offset" : offset,
                "reblog_info" : reblog_info,
                "notes_info" : notes_info,
                "npf" : npf}

        if not (specific_post_id == ""):
            json["specific_post_id"] = specific_post_id

        if not (filter == ""):
            json["filter"] = filter

        if not (before == ""):
            json["before"] = before

        # return the response
        return requests.get(request, params=json, auth=self.oauth)

    # queue list
    # requires `target_blog`, and `auth`
    # `target_blog` specifies the id of the blog that you are pulling queue data from
    # `auth` is system handled
    # `offset` defines the index to begin at in the complete posts list [0]
    # `limit` defines the number of posts to pull from the index [20] {max 20}
    # `filter` specifies the HTML format [""]
    def queueList(self, control_blog, offset=0, limit=20, filter=""):
        # build the request with the appropriate variables
        request = self.base_url+control_blog+"/posts/queue"
        # build json
        json = {"offset" : offset,
                "limit" : limit,
                "filter" : filter}
        # return the response
        return requests.get(request, params=json, auth=self.oauth)
        
    # reorder queue list
    # requires `target_blog`, `post_id`, and `auth`
    # `target_blog` specifies the id of the blog that you are reordering the queue of
    # `auth` is system handled
    # `post_id` specfies which post you want to reorder [0]
    # `insert_after` specfies which index or post id to insert the `post_id` after {0 is the top} [0]
    def reorderQueue(self, control_blog, post_id="", insert_after=0):
        # build the request with the appropriate variables
        request = self.base_url+control_blog+"/posts/queue/reorder"
        # build json
        json = {"post_id" : post_id, 
                "insert_after" : insert_after}
        # return the response
        return requests.post(request, params=json, auth=self.oauth)

    # shuffle queue list
    # requires `target_blog`, and `auth`
    # `target_blog` specifies the id of the blog that you are shuffling the queue of
    # `auth` is system handled
    def shuffleQueue(self, target_blog):
        # build the request with the appropriate variables
        request = self.base_url+target_blog+"/posts/queue/shuffle"
        # return the response
        return requests.post(request, auth=self.oauth)

    # draft list
    # requires `target_blog`, and `auth`
    # `target_blog` specifies the id of the blog that you are pulling draft list data from
    # `auth` is system handled
    # `before_id` is similar to offset but works backwards [0]
    # `filter` specifies the HTML format [""]
    def draftsList(self, target_blog, before_id=0, filter=""):
        # build the request with the appropriate variables
        request = self.base_url+target_blog+"/posts/draft"
        # build json
        json = {"before_id" : before_id,
                "filter" : filter}
        # return the response
        return requests.get(request, params=json, auth=self.oauth)

    # submission list
    # requires `target_blog`, and `auth`
    # `target_blog` specifies the id of the blog that you are pulling draft list data from
    # `auth` is system handled
    # `offset` defines the index to begin at in the complete posts list [0]
    # `filter` specifies the HTML format [""]
    def submissionsList(self, target_blog, offset=0, filter=""):
        # build the request with the appropriate variables
        request = self.base_url+target_blog+"/posts/submission"
        # build json
        json = {"filter" : filter,
                "offset" : offset}
        # return the response
        return requests.get(request, params=json, auth=self.oauth)

    # activity
    # requires `target_blog`, and `auth`
    # `target_blog` specifies the id of the blog that you are pulling activity data from
    # `auth` is system handled
    # `before` is a timestamp to get activity for before a certain point [request time]
    # `types` is the types of activity to respond with [[]]
    # `rollups` determines whether to merge similar bits of data [False]
    # `omit_post_ids` will filter out all specified post ids from the response [[]]
    def activity(self, target_blog, before="", types=[], rollups=False, omit_post_ids=[]):
        # build the request with the appropriate variables
        request = self.base_url+target_blog+"/notifications"
        # build json
        json = {"before" : before,
                "types" : types,
                "rollups" : rollups,
                "omit_post_ids" : omit_post_ids}
        # return the response
        return requests.get(request, params=json, auth=self.oauth)

    # fetch post
    # requires `target_blog`, and `auth`
    # `target_blog` specifies the id of the blog to pull a specific post from
    # `post_id` is the id of the post that you want to fetch
    # `auth` is system handled
    # `post_format` determines if the post should be fetched in "npf" or "legacy" mode ["npf"]
    def fetchPost(self, control_blog, post_id="", post_format="npf"):
        # convert post_id to string
        post_id = str(post_id)
        # build the request with the appropriate variables
        request = self.base_url+control_blog+"/posts/"+post_id
        # build json
        json = {"post_format" : post_format}
        # return the response
        return requests.get(request, params=json, auth=self.oauth)


    # post or reblog
    # requires `control_blog`, and `auth`
    # `control_blog` specifies the id of the blog that you are posting a post from
    # `npf_content` takes NPF-structured content data
    # `auth` is system handled
    # `npf_layout` takes NPF-structured layout data [""]
    # `state` determines if the post should be posted immediately or queued {"published" or "queued"} ["published"]
    # `publish_on` states a timestamp that the post should be published at when `state` is "quueued" ["Now"]
    # `date` states a timestamp that the post should be backdated to ["Now"]
    # `tags` specifies the tag(s) that the post should contain [[]]
    # `source_url` is the source attribution [""]
    # `send_to_twitter` sends the post to twitter automatically [False]
    # `is_private` determines whether an answer should be a private answer [False]
    # `slug` is the message to add to the post's permalink [""]
    # `interactability_reblog` decides who can interact by reblogging {"everyone" or "noone"} ["everyone"]
    # `hide_trail` determines if the reblog trail should be associated with your reblog [False]
    # `exclude_trail_items` is a list of items that should be excluded in the trail results [[]]
    def post(self, control_blog, target_blog="", post_id="", hide_trail=False, exclude_trail_items=[], npf_content=[], npf_layout=[], state="published", publish_on="Now", date="Now", tags=["test"], source_url="", send_to_twitter=False, is_private=True, slug="", interactability_reblog='everyone'):

        # ensure post_id is, in fact, a string
        post_id = str(post_id)

        # can tags be treated as a raw string?
        if not (tags == []):
            if (len(tags) > 1):
                i = 0
                # properly format the query and heirarchy of tags
                for tag in tags:
                    tags_string_final = tags_string_final + tag + ","
                    i += 1
                tags_string_final = tags_string_final[:-1]
            else:
                tags_string_final = str(tags[0])


        # adds required json params
        json = {"content" : npf_content,
                "layout" : npf_layout,
                "state" : state,
                "tags" : tags_string_final,
                "source_url" : source_url,
                "send_to_twitter" : send_to_twitter,
                "is_private" : is_private,
                "slug" : slug,
                "interactability_reblog" : interactability_reblog
               }

        if not (target_blog == "") and not (post_id == ""):
            # reblog mode

            blog = Blog(oauth_=self.oauth)

            target_post = blog.fetchPost(control_blog=target_blog, post_id=post_id).json()
            target_post_response = target_post['response']

            tumblelog_uuid = target_post_response['tumblelog_uuid']
            reblog_key = target_post_response['reblog_key']  

            # configure json from args
            reblog_json = {"parent_tumblelog_uuid" : tumblelog_uuid,
                           "parent_post_id" : post_id,
                           "reblog_key" : reblog_key,
                           "hide_trail" : hide_trail,
                           "exclude_trail_items" : exclude_trail_items,
                          }
            
            # join the two jsons together
            json.update(reblog_json)

        
        else:
            # post mode

            # if no specified content, fill with action description
            if (npf_content == []):
                npf_content = [{"type" : "text", "text" : "Automatically posted!"}]
                json['content'] = npf_content


        # adds time-specific universal params from args
        if not (publish_on == "Now"):
            json["publish_on"] = publish_on
        if not (date == "Now"):
            json["date"] = date

        # print(json)

        # build the request
        request = self.base_url+control_blog+"/posts"

        # return the response
        return requests.post(request, params=json, auth=self.oauth)
            


    # edit post
    # requires `control_blog`, `post_id`, and `auth`
    # `control_blog` specifies the id of the blog that you are posting a post from
    # `npf_content` takes NPF-structured content data
    # `auth` is system handled
    # `npf_layout` takes NPF-structured layout data [""]
    # `state` determines if the post should be posted immediately or queued {"published" or "queued"} ["published"]
    # `publish_on` states a timestamp that the post should be published at when `state` is "quueued" ["Now"]
    # `date` states a timestamp that the post should be backdated to ["Now"]
    # `tags` specifies the tag(s) that the post should contain [[]]
    # `source_url` is the source attribution [""]
    # `send_to_twitter` sends the post to twitter automatically [False]
    # `is_private` determines whether an answer should be a private answer [False]
    # `slug` is the message to add to the post's permalink [""]
    # `interactability_reblog` decides who can interact by reblogging {"everyone" or "noone"} ["everyone"]
    # `hide_trail` determines if the reblog trail should be associated with your reblog [False]
    # `exclude_trail_items` is a list of items that should be excluded in the trail results [[]]
    def editPost(self, control_blog, post_id=714876198768001024, npf_content = [], npf_layout=[], state="published", publish_on="Now", date="Now", tags=[""], source_url="", send_to_twitter=False, is_private=False, slug="", interactability_reblog='everyone', hide_trail=False, exclude_trail_items=[]):

        # ensure post_id is, in fact, a string
        post_id = str(post_id)

        
        # set default content to long-term nuclear warning messages
        if (npf_content == []):

            # random messages
            stock_texts=["This place is a message... and part of a system of messages... pay attention to it!",
                        "Sending this message was important to us. We considered ourselves to be a powerful culture.",
                        "This place is not a place of honor... no highly esteemed deed is commemorated here... nothing valued is here.",
                        "What is here was dangerous and repulsive to us. This message is a warning about danger.",
                        "The danger is in a particular location... it increases towards a center... the center of danger is here... of a particular size and shape, and below us.",
                        "The danger is still present, in your time, as it was in ours.",
                        "The danger is to the body, and it can kill.",
                        "The form of the danger is an emanation of energy.",
                        "The danger is unleashed only if you substantially disturb this place physically. This place is best shunned and left uninhabited."]

            # choose random message
            random_text = stock_texts[random.randint(0, len(stock_texts))]

            # set content
            npf_content = [{'type': 'text', 'text': random_text}]


        # can tags be treated as a raw string?
        if not (tags == []):
            if (len(tags) > 1):
                i = 0
                # properly format the query and heirarchy of tags
                for tag in tags:
                    tags_string_final = tags_string_final + tag + ","
                    i += 1
                tags_string_final = tags_string_final[:-1]
            else:
                tags_string_final = str(tags[0])

        blog = Blog(oauth_=self.oauth)

        target_post = blog.fetchPost(control_blog=control_blog, post_id=post_id).json()
        target_post_response = target_post['response']

        # print(target_post_response)

        # adds required json params
        json = {"content" : npf_content,
                "layout" : npf_layout,
                "state" : state,
                "tags" : tags_string_final,
                "source_url" : source_url,
                "send_to_twitter" : send_to_twitter,
                "is_private" : is_private,
                "slug" : slug,
                "interactability_reblog" : interactability_reblog
            }


        if not (target_post_response['trail'] == []):
            # reblog mode

            tumblelog_uuid = target_post_response['tumblelog_uuid']
            reblog_key = target_post_response['reblog_key']  

            # configure json from args
            reblog_json = {"parent_tumblelog_uuid" : tumblelog_uuid,
                        "parent_post_id" : post_id,
                        "reblog_key" : reblog_key,
                        "hide_trail" : hide_trail,
                        "exclude_trail_items" : exclude_trail_items,
                        }
        
            # join the two jsons together    
            json.update(reblog_json)
        
        else:
            # post mode

            # if no specified content, fill with action description
            if (npf_content == []):
                npf_content = [{"type" : "text", "text" : "Automatically posted!"}]
            


        # adds time-specific universal params from args
        if not (publish_on == "Now"):
            json["publish_on"] = publish_on
        if not (date == "Now"):
            json["date"] = date

        # print(json)
        # build request
        request = self.base_url+control_blog+"/posts/"+str(post_id)
        # return response
        return requests.put(request, params=json, auth=self.oauth)

    # delete
    # requires `control_blog`, `post_id`, and `auth`
    # `control_blog` is the id of the blog that you are deleting posts from
    # `post_id` is the id of the post you are deleting
    # `auth` is system handled
    def delete(self, control_blog, post_id):
        # set post_id
        post_id = str(post_id)
        # build request
        request = self.base_url+control_blog+"/post/delete"
        # build json
        json = {"id" : post_id}
        # return the response
        return requests.post(request, params=json, auth=self.oauth)

    # notes
    # requires `control_blog`, `api_key`, `post_id`, and `auth`
    # `control_blog` is the id of the blog that you are deleting posts from
    # `api_key` is system handled
    # `post_id` is the id of the post you are deleting
    # `auth` is system handled
    # `before_timestamp` returns notes from before the target timestamp [""]
    # `mode` determines what kind of responses to return ("all", "likes", "conversation", "rollup", "reblogs_with_tags") ["all"]
    def notes(self, target_blog, post_id, before_timestamp="", mode="all"):
        # post_id is string
        post_id = str(post_id) #pulls the pinned post
        # build request
        request = self.base_url+target_blog+"/notes?id="+post_id+"&api_key="+self.api_key
        # build json
        json = {"mode" : mode,
                "before_timestamp" : before_timestamp}
        # return the response
        return requests.get(request, params=json, auth=self.oauth)
