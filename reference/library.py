# Tumblr API Library in Python
# The following is the current record of the Tumblr API in Python designed and written by cubic.
# This is in service of the BotBreaker project.
# Ver 0.1.0

# THIS IS A JUMBLE. MORE REFINED CODE TO COME!

# imports
import random
import requests
from requests_oauthlib import OAuth1

# creds
creds_file = open("./../Credentials/botbreaker.txt", "r")

uuid =          creds_file.readline()[:-1] # uuid on line one
api_key =       creds_file.readline()[:-1] # api_key on line two
api_secret =    creds_file.readline()[:-1] # api_secret on line three
oauth_key =     creds_file.readline()[:-1] # oauth_key on line four
oauth_secret =  creds_file.readline()[:-1] # oauth_secret on line five

creds_file.close()

oauth = OAuth1(api_key, client_secret=api_secret,
               resource_owner_key=oauth_key,
               resource_owner_secret=oauth_secret)

# blog identifiers
own_uuid = "botbreaker"             # botbreaker dev blog
bot_target_uuid = "teamredpointone" # target blog
bot_targets = ["teamredpointone"]   # list-version for list needing formats

# all requests start thus
base_url = "https://api.tumblr.com/v2/"
blog_base_url = base_url+"blog/"
user_base_url = base_url+"user/"

# info
# requires `target_blog`, `api_key`, and `auth`
# `target_blog` is the id of the blog to pull info data from
# `api_key` is system handled
# `auth` is system handled
# `fields` limits the data returned to the specified attributes along with some extra data [[]]
def info(auth=oauth, target_blog=own_uuid, api_key=api_key, fields=[]):
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

        request = blog_base_url+target_blog+"/info?api_key="+api_key+"&fields[blogs]="+fields_final+"?is_following_you,?duration_blog_following_you,?duration_following_blog,?timezone,?timezone_offset"
    else:
        request = blog_base_url+target_blog+"/info?api_key="+api_key
        
    # return the response
    return requests.get(request, auth=auth)

# avatar
# requires `target_blog`, `auth`, and `size`
# `target_blog` specifies the id of the blog to pull avatar data from 
# `auth` is system handled
# `size` is the width and height you want the square image to be [64]
def avatar(auth=oauth, target_blog=own_uuid, size=64):
    # build the request with the appropriate variables
    request = blog_base_url+target_blog+"/avatar/"+str(size)
    # return the response
    return requests.get(request, auth=auth)

# blockedList
# requires `target_blog`, and `auth`
# `target_blog` specifies the id of the blog to pull blocked list data from
# ` auth` is system handled
# `offset` defines the index to begin at in the complete blocked list [0]
# `limit` defines the number of posts to pull from the index [20] {max 20}
def blockedList(auth=oauth, target_blog=own_uuid, offset=0, limit=20):
    # build the request with the appropriate variables
    request = blog_base_url+target_blog+"/blocks"
    # return the response
    return requests.get(request, json={"offset" : offset, "limit" : limit}, auth=auth)

# block
# requires `target_blog`, `control_blog`, and `auth`
# `target_blog` specifies the id of the blog to block
# `control_blog` specifies the id of the blog to block from
# `auth` is system handled
def block(auth=oauth, control_blog=own_uuid, target_blog=bot_target_uuid):
    # build the request with the appropriate variables
    request = blog_base_url+control_blog+"/blocks"
    # return the response
    return requests.post(request, json={"blocked_tumblelog" : target_blog}, auth=auth)

# bulkBlock
# requires `target_blogs`, `control_blog`, and `auth`
# `target_blogs` specifies the list of ids of blogs to block
# `control_blog` specifies the id of the blog to block from
# `auth` is system handled
def bulkBlock(auth=oauth, control_blog=own_uuid, target_blogs=bot_targets):
    # declare final processed blogs string
    target_blogs_final = ""

    # process the target blogs input
    for blog in target_blogs:
        target_blogs_final = target_blogs_final + str(blog) + ","
    target_blogs_final = target_blogs_final[:-1]

    # build the request with the appropriate variables
    request = blog_base_url+control_blog+"/blocks/bulk"
    # return the response
    return requests.post(request, json={"blocked_tumblelogs" : target_blogs_final}, auth=auth)

# unblock
# requires `control_blog`, `target_blog`, and `auth`
# `target_blog` specifies the id of the blog to unblock
# `control_blog` specifies the id of the blog to unblock from
# `auth` is system handled
def unblock(auth=oauth, control_blog=own_uuid, target_blog=bot_target_uuid):
    # build the request with the appropriate variables
    request = blog_base_url+control_blog+"/blocks"
    # return the response
    return requests.delete(request, json={"blocked_tumblelog" : target_blog}, auth=auth)

# likes
# requires `target_blog`, `api_key`, `auth`
# `target_blog` specifies the id of the blog to pull likes data from
# `api_key` is system handled
# `auth` is system handled
# `offset` defines the index to begin at in the complete blocked list [0]
# `limit` defines the number of posts to pull from the index [20] {max 20}
# `before` is the timestamp (in seconds) before which the system will look for data [-1]
# `after` is the timestamp (in seconds) after which the system will look for data [-1]
def blogLikesList(auth=oauth, target_blog=own_uuid, api_key=api_key, offset=0, limit=20, before=-1, after=-1):
    # build the request with the appropriate variables
    request = blog_base_url+target_blog+"/likes?api_key="+api_key
    
    # constructs data given in the correct order and then returns the response
    # hierarchy is thus: `before` -> `after` -> `offset`
    # `limit` can coexist with `before` or `after` or `offset`
    # but `before` and `after` and `offset` cannot coexist
    if not (before == -1):
        return requests.get(request, json={"limit" : limit, "before" : before}, auth=auth)
    elif not (after == -1):
        return requests.get(request, json={"limit" : limit, "after" : after}, auth=auth)
    elif not (offset == 0):
        if (offset > 1000):
            print("Offset exceeds 1000. Use before or after.")
            return ""

        return requests.get(request, json={"limit" : limit, "offset" : offset}, auth=auth)
    else:
        return requests.get(request, json={"limit" : limit, "offset" : offset}, auth=auth)

# following
# requires `target_blog`, and `auth`
# `target_blog` specifies the id of the blog to pull following list data from
# `auth` is system handled
# `offset` defines the index to begin at in the complete following list [0]
# `limit` defines the number of following to pull from the index [20] {max 20}
def blogFollowingList(auth=oauth, target_blog=own_uuid, offset=0, limit=20):
    # build the request with the appropriate variables
    request = blog_base_url+target_blog+"/following"
    # return the response
    return requests.get(request, json={"limit" : limit, "offset" : offset}, auth=auth)

# followers
# requires `target_blog`, and `auth`
# `target_blog` specifies the id of the blog to pull follower list data from
# `auth` is system handled
# `offset` defines the index to begin at in the complete follower list [0]
# `limit` defines the number of followers to pull from the index [20] {max 20}
def followersList(auth=oauth, target_blog=own_uuid, offset=0, limit=20):
    # build the request with the appropriate variables
    request = blog_base_url+target_blog+"/followers"
    # return the response
    return requests.get(request, json={"limit" : limit, "offset" : offset}, auth=auth)

# followedBy
# requires `control_blog`, `target_blog`, and `auth`
# `control_blog` specifies the id of the blog you are checking is being followed by `target_blog`
# `target_blog` specifies the id of the blog you are checking is following `control_blog`
# `auth` is system handled
def followedBy(auth=oauth, control_blog=own_uuid, target_blog=bot_target_uuid):
    # build the request with the appropriate variables
    request = blog_base_url+control_blog+"/followed_by?query="+target_blog
    # return the response
    return requests.get(request, auth=auth)

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
def postsList(auth=oauth, target_blog=own_uuid, api_key=api_key, type="", specific_post_id="", tags=[], offset=0, limit=20, reblog_info=True, notes_info=True, filter="", before="", npf=True):
    # begin request construction
    request = blog_base_url+target_blog+"/posts"

    # add type if not default [""]
    if not (type == ""):
        request += "/"+type

    # add api key
    request = request+"?api_key="+api_key

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
    return requests.get(request, json=json, auth=auth)

# queue list
# requires `target_blog`, and `auth`
# `target_blog` specifies the id of the blog that you are pulling queue data from
# `auth` is system handled
# `offset` defines the index to begin at in the complete posts list [0]
# `limit` defines the number of posts to pull from the index [20] {max 20}
# `filter` specifies the HTML format [""]
def queueList(auth=oauth, control_blog=own_uuid, offset=0, limit=20, filter=""):
    # build the request with the appropriate variables
    request = blog_base_url+control_blog+"/posts/queue"
    # return the response
    return requests.get(request, json={"offset" : offset, "limit" : limit, "filter" : filter}, auth=auth)
    
# reorder queue list
# requires `target_blog`, `post_id`, and `auth`
# `target_blog` specifies the id of the blog that you are reordering the queue of
# `auth` is system handled
# `post_id` specfies which post you want to reorder [0]
# `insert_after` specfies which index or post id to insert the `post_id` after {0 is the top} [0]
def reorderQueueList(auth=oauth, control_blog=own_uuid, post_id="", insert_after=0):

    # if the queue list is empty return "MTQ" (clever right?)
    if (queueList(control_blog=control_blog).json()['response']['posts'] == []):
        return "MTQ"

    # if given no 
    if (post_id == ""):
        try:
            post_id = queueList(control_blog=control_blog).json()['response']['posts'][0]['id']
        except IndexError:
            pass

    # build the request with the appropriate variables
    request = blog_base_url+control_blog+"/posts/queue/reorder"
    # return the response
    return requests.post(request, json={"post_id" : post_id, "insert_after" : insert_after}, auth=auth)

# shuffle queue list
# requires `target_blog`, and `auth`
# `target_blog` specifies the id of the blog that you are shuffling the queue of
# `auth` is system handled
def shuffleQueueList(auth=oauth, target_blog=own_uuid):
    # build the request with the appropriate variables
    request = blog_base_url+target_blog+"/posts/queue/shuffle"
    # return the response
    return requests.post(request, auth=auth)

# draft list
# requires `target_blog`, and `auth`
# `target_blog` specifies the id of the blog that you are pulling draft list data from
# `auth` is system handled
# `before_id` is similar to offset but works backwards [0]
# `filter` specifies the HTML format [""]
def draftList(auth=oauth, target_blog=own_uuid, before_id=0, filter=""):
    # build the request with the appropriate variables
    request = blog_base_url+target_blog+"/posts/draft"
    # return the response
    return requests.get(request, json={"before_id" : before_id, "filter" : filter}, auth=auth)

# submission list
# requires `target_blog`, and `auth`
# `target_blog` specifies the id of the blog that you are pulling draft list data from
# `auth` is system handled
# `offset` defines the index to begin at in the complete posts list [0]
# `filter` specifies the HTML format [""]
def submissionList(auth=oauth, target_blog=own_uuid, offset=0, filter=""):
    # build the request with the appropriate variables
    request = blog_base_url+target_blog+"/posts/submission"
    # return the response
    return requests.get(request, json={"offset" : offset, "filter" : filter}, auth=auth)

# activity
# requires `target_blog`, and `auth`
# `target_blog` specifies the id of the blog that you are pulling activity data from
# `auth` is system handled
# `before` is a timestamp to get activity for before a certain point [request time]
# `types` is the types of activity to respond with [[]]
# `rollups` determines whether to merge similar bits of data [False]
# `omit_post_ids` will filter out all specified post ids from the response [[]]
def activity(auth=oauth, target_blog=own_uuid, before="", types=[], rollups=False, omit_post_ids=[]):
    # build the request with the appropriate variables
    request = blog_base_url+target_blog+"/notifications"
    # return the response
    return requests.get(request, json={"before" : before, "types" : types, "rollups" : rollups, "omit_post_ids" : omit_post_ids}, auth=auth)

# fetch post
# requires `target_blog`, and `auth`
# `target_blog` specifies the id of the blog to pull a specific post from
# `post_id` is the id of the post that you want to fetch
# `auth` is system handled
# `post_format` determines if the post should be fetched in "npf" or "legacy" mode ["npf"]
def fetchPost(auth=oauth, control_blog=own_uuid, post_id="", post_format="npf"):
    # convert post_id to string
    post_id = str(post_id)
    # build the request with the appropriate variables
    request = blog_base_url+control_blog+"/posts/"+post_id
    # return the response
    return requests.get(request, json={"post_format" : post_format}, auth=auth)


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
def post(auth=oauth, control_blog=own_uuid, target_blog="", post_id="", hide_trail=False, exclude_trail_items=[], npf_content=[], npf_layout=[], state="published", publish_on="Now", date="Now", tags=["test"], source_url="", send_to_twitter=False, is_private=True, slug="", interactability_reblog='everyone'):

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

        target_post = fetchPost(control_blog=target_blog, post_id=post_id).json()
        target_post_response = target_post['response']

        # print(target_post_response)


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
    request = blog_base_url+control_blog+"/posts"

    # return the response
    return requests.post(request, json=json, auth=auth)
        


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
def editPost(auth=oauth, control_blog=own_uuid, post_id=714876198768001024, npf_content = [], npf_layout=[], state="published", publish_on="Now", date="Now", tags=[""], source_url="", send_to_twitter=False, is_private=False, slug="", interactability_reblog='everyone', hide_trail=False, exclude_trail_items=[]):

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


    target_post = fetchPost(control_blog=control_blog, post_id=post_id).json()
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
    request = blog_base_url+control_blog+"/posts/"+str(post_id)
    # return response
    return requests.put(request, json=json, auth=auth)

# delete
# requires `control_blog`, `post_id`, and `auth`
# `control_blog` is the id of the blog that you are deleting posts from
# `post_id` is the id of the post you are deleting
# `auth` is system handled
def delete(auth=oauth, control_blog=own_uuid, post_id=712889496527667200):
    # set post_id
    post_id = str(post_id)
    # build request
    request = blog_base_url+control_blog+"/post/delete"
    # return the response
    return requests.post(request, json={"id" : post_id}, auth=auth)

# notes
# requires `control_blog`, `api_key`, `post_id`, and `auth`
# `control_blog` is the id of the blog that you are deleting posts from
# `api_key` is system handled
# `post_id` is the id of the post you are deleting
# `auth` is system handled
# `before_timestamp` returns notes from before the target timestamp [""]
# `mode` determines what kind of responses to return ("all", "likes", "conversation", "rollup", "reblogs_with_tags") ["all"]
def notes(auth=oauth, api_key=api_key, target_blog=own_uuid, post_id=712885306404290561, before_timestamp="", mode="all"):
    # post_id is string
    post_id = str(post_id) #pulls the pinned post
    # build request
    request = blog_base_url+target_blog+"/notes?id="+post_id+"&api_key="+api_key
    # return the response
    return requests.get(request, json={"mode" : mode, "before_timestamp" : before_timestamp}, auth=auth)

# user info
# requires `auth`
# `auth` is system handled
def userInfo(auth=oauth):
    # build request
    request = user_base_url+"info"
    # return response
    return requests.get(request, auth=auth)

# user limits
# requires `auth`
# `auth` is system handled
def userLimits(auth=oauth):
    # build request
    request = user_base_url+"limits"
    # return response
    return requests.get(request, auth=auth)

# user dashboard
# requires `auth`
# `auth` is system handled
def userDashboard(auth=oauth, limit=20, offset=0, type="", since_id=0, reblog_info=True, notes_info=True, npf=True):
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
    request = user_base_url+"dashboard"
    # return response
    return requests.get(request, json=json, auth=auth)

# user likes
# requires `auth`
# `auth` is system handled
# `offset` defines the index to begin at in the complete blocked list [0]
# `limit` defines the number of posts to pull from the index [20] {max 20}
# `before` is the timestamp (in seconds) before which the system will look for data [-1]
# `after` is the timestamp (in seconds) after which the system will look for data [-1]
def userLikesList(auth=oauth, limit=20, offset=0, before=0, after=0):
    request = user_base_url+"likes"

    # constructs data given in the correct order and then returns the response
    # hierarchy is thus: `before` -> `after` -> `offset`
    # `limit` can coexist with `before` or `after` or `offset`
    # but `before` and `after` and `offset` cannot coexist
    if not (before == -1):
        return requests.get(request, json={"limit" : limit, "before" : before}, auth=auth)
    elif not (after == -1):
        return requests.get(request, json={"limit" : limit, "after" : after}, auth=auth)
    elif not (offset == 0):
        if (offset > 1000):
            print("Offset exceeds 1000. Use before or after.")
            return ""

        return requests.get(request, json={"limit" : limit, "offset" : offset}, auth=auth)
    else:
        return requests.get(request, json={"limit" : limit, "offset" : offset}, auth=auth)

# user following
# requires `auth`
# `auth` is system handled
# `offset` defines the index to begin at in the complete blocked list [0]
# `limit` defines the number of posts to pull from the index [20] {max 20}
def userFollowingList(auth=oauth, limit=20, offset=0):
    # build requests
    request = user_base_url+"following"
    # return response
    return requests.get(request, json={"limit" : limit, "offset" : offset}, auth=auth)

# follow
# requires `auth`, and `url` or `email`
# `auth` is system handled
# `url` is the url of the blog to follow
# `email` of the blog to follow provided its
def follow(auth=oauth, url="https://www.tumblr.com/"+bot_target_uuid, email=""):
    # build requests
    request = user_base_url+"follow"
    # declare json
    json = {}
    
    # decide if url or email should be used
    if (url == ""):
        json['email'] = email
    else:
        json['url'] = url

    # return responses
    return requests.post(request, json=json, auth=auth)

# unfollow
# requires `auth`, and `url`
# `auth` is system handled
# `url` is the url of the blog to unfollow
def unfollow(auth=oauth, url="https://www.tumblr.com/"+bot_target_uuid):
    request = user_base_url+"unfollow"
    return requests.post(request, json={"url" : url} , auth=auth)


# like
# requires `auth`, `post_id`, and `reblog_key`
# `auth` is system handled
# `post_id` is the id of the post to like
# `reblog_key` is the reblog key of the post to like
def like(auth=oauth, post_id=postsList(target_blog=bot_target_uuid).json()['response']['posts'][0]['id'], reblog_key=postsList(target_blog=bot_target_uuid).json()['response']['posts'][0]['reblog_key']):
    # build request
    request = user_base_url+"like"
    # return response
    return requests.post(request, json={"id" : post_id, "reblog_key" : reblog_key} , auth=auth)

# unlike
# requires `auth`, `post_id`, and `reblog_key`
# `auth` is system handled
# `post_id` is the id of the post to unlike
# `reblog_key` is the reblog key of the post to unlike
def unlike(auth=oauth, post_id=postsList(target_blog=bot_target_uuid).json()['response']['posts'][0]['id'], reblog_key=postsList(target_blog=bot_target_uuid).json()['response']['posts'][0]['reblog_key']):
    # build request
    request = user_base_url+"unlike"
    # return response
    return requests.post(request, json={"id" : post_id, "reblog_key" : reblog_key} , auth=auth)

# get filtered tags
# requires `auth`
# `auth` is system handled
def getFilteredTags(auth=oauth):
    request = user_base_url+"filtered_tags"
    return requests.get(request, auth=auth)

# add tag filter
# requires `auth`
# `auth` is system handled
def addTagFilter(auth=oauth, filtered_tags=["test"]):
    request = user_base_url+"filtered_tags"
    return requests.post(request, json={"filtered_tags" : filtered_tags}, auth=auth)

# remove tag filter
# requires `auth`
# `auth` is system handled
def removeTagFilter(auth=oauth, tag="test"):

    if (getFilteredTags().json()['response']['filtered_tags'] == []):
        return "MTF"

    request = user_base_url+"filtered_tags/"+str(tag)
    return requests.delete(request, auth=auth)

# tagged
# requires `auth` or `api_key`, and `tag`
# `auth` is system handled
# `api_key` is system handled
# `tag` is the target tag that you want to pull info from
# `before` determines the timestamp before which the posts should be pulled [""]
# `limit` is the number of posts to return per response if more than this number is found (0-20) [20]
# `filter` specifies the return format
def tagged(auth=oauth, api_key=api_key, tag="test", before="", limit=20, filter=""):

    # builds base url
    request = base_url+"tagged?api_key="+api_key+"&tag="+tag

    # adds json
    json = {"limit" : limit,
            "filter" : filter}

    if not (before == ""):
        json["before"] = before

    # returns response
    return requests.get(request, json=json, auth=auth)


# check
# checks the above systems are working
def check(function, function_name, passing_status_codes):
    for status_code in passing_status_codes:
        if (hasattr(function, "status_code")):
            if (function.status_code == status_code):
                print((function_name.upper() + " CHECK: ").ljust(30) + str(status_code) + " PASS")
                return "PASS"
        else:
            if (function == status_code):
                print((function_name.upper() + " CHECK: ").ljust(30) + str(status_code) + " PASS")
                return "PASS"
        
    print((function_name.upper() + " CHECK: ").ljust(30) + str(function.status_code) + " FAIL [expected 200, 201 or similar]")
    return "FAIL"

func_list = [info,
             avatar,
             blockedList,
             block,
             bulkBlock,
             unblock,
             blogLikesList,
             blogFollowingList,
             followersList,
             followedBy,
             postsList,
             queueList,
             reorderQueueList,
             shuffleQueueList,
             draftList,
             submissionList,
             activity,
             post,                                                    #post
             post(target_blog=own_uuid, post_id=714876198768001024),  #reblog's the edit post
             fetchPost,
             editPost,
             delete,
             notes,
             userInfo,
             userLimits,
             userDashboard,
             userLikesList,
             userFollowingList,
             follow,
             unfollow,
             like,
             unlike,
             getFilteredTags,
             addTagFilter,
             removeTagFilter,
             tagged]

func_name_list = ["info",
                  "avatar",
                  "blocked list",
                  "block",
                  "bulk block",
                  "unblock",
                  "likes list",
                  "following list",
                  "followers list",
                  "followed by",
                  "posts list",
                  "queue list",
                  "reorder queue list",
                  "shuffle queue list",
                  "draft list",
                  "submission list",
                  "activity",
                  "post",
                  "reblog",
                  "fetch post",
                  "edit post",
                  "delete",
                  "notes",
                  "user info",
                  "user limits",
                  "user dashboard",
                  "userLikesList",
                  "userFollowingList",
                  "follow",
                  "unfollow",
                  "like",
                  "unlike",
                  "get filtered tags",
                  "add tag filter",
                  "remove tag filter",
                  "tagged"]

# func_args =     []

passing_status_codes = [200,
                        201,
                        "MTQ",
                        "MTF"]

i = 0
passed = 0
failed = 0
failure_report = "FAILED COMPONENTS:\n"

for func in func_list:
    
    if (callable(func)):
        if (check(func(), func_name_list[i], passing_status_codes) == "PASS"): 
            passed += 1
        else:
            failure_report += (func_name_list[i].upper() + ": ").ljust(29) + " " + str(func().status_code) + " FAIL [expected 200, 201 or similar]\n"
            failed += 1

    else:
        if (check(func, func_name_list[i], passing_status_codes) == "PASS"): 
            passed += 1
        else:
            failure_report += (func_name_list[i].upper() + ": ").ljust(29) + " " + str(func().status_code) + " FAIL [expected 200, 201 or similar]\n"
            failed += 1

    i += 1

if (passed == i):
    print("ALL PASSED")
else:
    print(str(passed).rjust(2, "0") + " PASSED")
    print(str(failed).rjust(2, "0") + " FAILED")
    print(failure_report)
