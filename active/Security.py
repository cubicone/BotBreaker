import random
import requests
from requests_oauthlib import OAuth1
from User import User
import os

class Security:
    
    def __init__(self, blog_name):
        # open creds file
        creds_file = open(f"./../Credentials/{blog_name}.txt", "r")

        self.uuid =          creds_file.readline()[:-1] # uuid on line one
        self.api_key =       creds_file.readline()[:-1] # api_key on line two
        self.api_secret =    creds_file.readline()[:-1] # api_secret on line three
        self.oauth_key =     creds_file.readline()[:-1] # oauth_key on line four
        self.oauth_secret =  creds_file.readline()[:-1] # oauth_secret on line five
        
        # close creds file
        creds_file.close()

        # no oauth key found suggests no further entries in creds file
        # this version is not written to file because they are temporary credentials
        if (self.oauth_key == ""):

            # use what info we already have
            oauth = OAuth1(client_key=self.api_key, client_secret=self.api_secret)

            # request token
            request = requests.post("https://www.tumblr.com/oauth/request_token", auth=oauth)
            request_string = request.text

            # parse those bad bois
            self.oauth_key = request_string.split("=", 1)[1].split("&", 1)[0]
            self.oauth_secret = request_string.split("=", 2)[2].split("&", 1)[0]

    # return all information gathered in the above init
    def getDetails(self):
        # finally, return listed information
        return self.uuid, self.api_key, self.api_secret, self.oauth_key, self.oauth_secret

    # avaliability
    def availability(self):
        # list of all blogs theoretically active and ready
        blogs = ["teambluepointone"]
        # results table
        availability = {}

        # check all blogs
        for blog in blogs:
            try:
                # get security file on current blog
                current_sec = Security(blog)

                # get user functions on current blog authentication
                user = User(current_sec)

                # if the limits returned nicely, this can be seen as the unit being ready
                if (user.limits().status_code == 200):
                    # readyness is marked with a 1
                    availability[blog] = 1

                # if the status code is not a pass, some error occoured
                else:
                    # non-readyness is marked with a -1
                    availability[blog] = -1
            
            # no credentials file associated with the target user
            except FileNotFoundError:
                availability[blog] = -1
            
        return availability

    # get connections which can be made right now
    def getActiveConnections(self):
        # get availability list
        availability = self.availability()

        # list for storing avalible connections from the above dictionary
        available_connections = []

        for blog in availability:

            current_value = availability[blog]
            # -1 is a fail, 1 is a pass
            if (current_value > 0):
                available_connections.append(blog)

        return available_connections

    # get connections which are down or error-filled
    def getDormantConnections(self):
        # get availability list
        availability = self.availability()

        # list for storing avalible connections from the above dictionary
        dormant_connections = []

        for blog in availability:

            current_value = availability[blog]
            # -1 is a fail, 1 is a pass
            if (current_value < 0):
                dormant_connections.append(blog)

        return dormant_connections

    # get connection from avalible connections
    def getConnection(self):
        # list of all active connections
        active_connections = self.getActiveConnections()
        # number of active connections
        num_active_connections = len(active_connections)

        if (num_active_connections == 0):
            return
        
        # random connection from list
        return active_connections[random.randint(0, num_active_connections-1)]
        

