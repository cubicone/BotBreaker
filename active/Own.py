from requests_oauthlib import OAuth1
import requests
from Blog import Blog
from User import User

creds_file = open("./../Credentials/botbreaker.txt", "r")

uuid =          creds_file.readline()[:-1] # uuid on line one
api_key =       creds_file.readline()[:-1] # api_key on line two
api_secret =    creds_file.readline()[:-1] # api_secret on line three
oauth_key =     creds_file.readline()[:-1] # oauth_key on line four
oauth_secret =  creds_file.readline()[:-1] # oauth_secret on line five

creds_file.close()

blog = Blog(uuid=uuid, api_key=api_key, api_secret=api_secret, oauth_key=oauth_key, oauth_secret=oauth_secret)
user = User(uuid, api_key, api_secret, oauth_key, oauth_secret)

class Own:
    
    # constructors for User
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
        self.base_url = "https://api.tumblr.com/v2/user/"

    blog = Blog(uuid, api_key, api_secret, oauth_key, oauth_secret)
    user = User(uuid, api_key, api_secret, oauth_key, oauth_secret)

    # bulk blog likes list
    # requires `target_blog`, and `return_type`
    # `target_blog` is the blog to fetch results from
    # `return_type` is the type of items to return
    # `num_results` determines how many results to return
    def bulkList(self, target_blog, target_type, num_results=240):

        # find
        match target_type:
            case "blocked":
                total_results = len(blog.blockedList(target_blog).json()['response']['blocked_tumblelogs'])
            case "posts":
                total_results = blog.postsList(target_blog).json()['response']['total_posts']
            case "blog likes":
                total_results = blog.likesList(target_blog).json()['response']['liked_count']
            case "user likes":
                total_results = user.likesList().json()['response']['liked_count']
            case "blog following":
                total_results = blog.followingList(target_blog).json()['response']['total_blogs']
            case "blog followers":
                total_results = blog.followersList(target_blog).json()['response']['total_users']
            case "user following":
                total_results = user.followingList().json()['response']['total_blogs']
            case "queue":
                total_results = len(blog.queueList(target_blog).json()['response']['posts'])
            case "drafts":
                total_results = len(blog.draftsList(target_blog).json()['response']['posts'])
            case "submissions":
                total_results = len(blog.submissionsList(target_blog).json()['response']['posts'])
            case "":
                return "Failed. Empty target type."
            case _:
                return "Failed. Cannot identify target type."

        num_results = int(num_results)

        # total number in the target list
        # total_likes = blog.likesList(target_blog=target_blog).json()['response']['liked_count']
        # if num results exceeds total possible results, return them all
        if (num_results > total_results):
            num_results = total_results
        # or if the results is blank
        elif (num_results == ""):
            # and the target list total is less than 241, return them all
            if (total_results <= 240):
                num_results = total_results
            # if they exceed 240, cap the results at 240
            else:
                num_results = 240

        # num results will stay the same, however, if it is a number value less than the total list number

        # number of requests to pull at once
        limit = 20
        # if num results exceeds total possible results, they will finish on the first trail. Set the limit to the desired number of results.
        if (num_results < limit):
            limit = num_results

        # start fetching loop counter
        i = 0
        # to return the final result
        results = []
        
        # start fetching loop
        while True:

            # before anything, check if you have exceeded the result number
            if ((i*limit) > num_results):
                break

            try:
                match target_type:
                    case "blocked":
                        results += blog.blockedList(target_blog=target_blog, offset=(i*limit), limit=limit).json()['response']['blocked_tumblelogs']
                    case "posts":
                        results += blog.postsList(target_blog=target_blog, offset=(i*limit), limit=limit).json()['response']['posts']
                    case "blog likes":
                        results += blog.likesList(target_blog=target_blog, offset=(i*limit), limit=limit).json()['response']['liked_posts']
                    case "user likes":
                        results += user.likesList(target_blog=target_blog, offset=(i*limit), limit=limit).json()['response']['liked_posts']
                    case "blog following":
                        results += blog.followingList(target_blog=target_blog, offset=(i*limit), limit=limit).json()['response']['blogs']
                    case "blog followers":
                        results += blog.followersList(target_blog=target_blog, offset=(i*limit), limit=limit).json()['response']['users']
                    case "user following":
                        results += user.followingList(target_blog=target_blog, offset=(i*limit), limit=limit).json()['response']['blog']
                    case "queue":
                        results += blog.queueList(target_blog=target_blog, offset=(i*limit), limit=limit).json()['response']['posts']
                    case "drafts":
                        results += blog.draftsList(target_blog=target_blog, offset=(i*limit), limit=limit).json()['response']['posts']
                    case "submissions":
                        results += blog.submissionsList(target_blog=target_blog, offset=(i*limit), limit=limit).json()['response']['posts']
                    case _:
                        break
            except:
                # in any parts fail after this point, there probably aren't any results left
                break

            i += 1
        
        return results

    def getAttributeList(self, list_of_objects, attribute):

        if not (isinstance(list_of_objects, list)):
            return "Failed: Object passed is not a list.\n " + list_of_objects

        results = []

        for object in list_of_objects:
            if attribute in object:
                results.append(object[str(attribute)])
            else:
                results.append("")

        return results

own = Own(uuid=uuid, api_key=api_key, api_secret=api_secret, oauth_key=oauth_key, oauth_secret=oauth_secret)
