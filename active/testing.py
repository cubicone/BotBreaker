import random
from Own import Own
# from Blog import Blog
from User import User
# from Crawler import Crawler
from Security import Security
import requests
import threading
from requests_oauthlib import OAuth1

sec = Security("botbreaker")
own = Own(sec)
# user = User(sec)
# blog = Blog(sec)
# crawler = Crawler(sec)

# creds_file = open(f"./../Credentials/botbreaker.txt", "r")

# uuid =          creds_file.readline()[:-1] # uuid on line one
# api_key =       creds_file.readline()[:-1] # api_key on line two
# api_secret =    creds_file.readline()[:-1] # api_secret on line three

# creds_file.close()

# oauth = OAuth1(client_key=api_key, client_secret=api_secret)

# request = requests.post("https://www.tumblr.com/oauth/request_token", auth=oauth)
# request_string = request.text

# oauth_token = request_string.split("=", 1)[1].split("&", 1)[0]
# oauth_token_secret = request_string.split("=", 2)[2].split("&", 1)[0]

# print(request_string)
# print(oauth_token)
# print(oauth_token_secret)

# random.randint(0, s)

print(sec.getDetails())