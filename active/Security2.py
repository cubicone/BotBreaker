# Tumblr API Security Functions
# The following is an organised, usable set of all functions which pertain to Security actions (all of which require OAuth1)
# This is in service of the BotBreaker project
# Ver 0.0.1

# import required libraries


class Security2:
    # constructor for Security
    # takes target blog for security object
    def __init__(self, target_blog_):
        self.target_blog = target_blog_

    def loadCredentials(self):
        # open credentials file
        credentials_file = open(f"./../Credentials/{self.target_blog}.txt", "r")

        # pull specific details from file
        self.uuid = credentials_file.readline()[:-1]  # uuid on ln 1
        self.api_key = credentials_file.readline()[:-1]  # api_key on ln 2
        self.api_secret = credentials_file.readline()[:-1]  # api_secret on ln 3
        self.oauth_key = credentials_file.readline()[:-1]  # oauth_key on ln 4
        self.oauth_secret = credentials_file.readline()[:-1]  # oauth_secret on ln 5

        # close credentials file
        credentials_file.close()

        # no oauth key suggests that there is no further entries in creds file
        # or no usable data
        # this is the point at which you get temporary credentials

        # TO BE WRITTEN

    # Here follow the gets and sets

    # there are no sets used at this point

    # these are the gets of all variables
    def getUUID(self):
        return self.uuid

    def getApiKey(self):
        return self.api_key

    def getApiSecret(self):
        return self.api_secret

    def getOauthKey(self):
        return self.oauth_key

    def getOauthSecret(self):
        return self.oauth_secret

    def getDetails(self):
        return (
            self.getUUID(),
            self.getApiKey(),
            self.getApiSecret(),
            self.getOauthKey(),
            self.getOauthSecret(),
        )
