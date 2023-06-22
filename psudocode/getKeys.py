# from requests_oauthlib import OAuth1Session
# import webbrowser

# key = "MLxGIPfvoalHo3pXO490QlRFIH7DQdmV8ZfAXr4inGoF5dVURl"
# secret = "tCnjsesMT0sCZM1uGAAeO6xK7Z138L8vqQJ5JbbhQbRlhJJMsh"
# uuid = 'teambluepointone'

# request_token_url = "https://www.tumblr.com/oauth/request_token"
# authorization_base_url = "https://www.tumblr.com/oauth/authorize"
# access_token_url = "https://www.tumblr.com/oauth/access_token"

# tumblr = OAuth1Session(key, client_secret=secret, callback_uri="https://www.tumblr.com/dashboard")
# tumblr.fetch_request_token(request_token_url)

# authorization_url = tumblr.authorization_url(authorization_base_url)
# print("Go here to authorize: " + authorization_url)

# redirect_response = input("Paste redirect URL here: ")
# tumblr.parse_authorization_response(redirect_response)

# tumblr.fetch_access_token(access_token_url)

# print(tumblr.get("https://api.tumblr.com/v2/user/dashboard").text)

# # https://www.tumblr.com/dashboard?oauth_token=SAa2kGM9x2kDR5Tb9KLFcGoO7vBKt2STiH401XXb5Qh3ilC3fr&oauth_verifier=RdFLnsxl5KWy0qvEb4HyjlGIyeWDp6lTtug4Gl373bzU2uPBMC#_=_

# # https://www.tumblr.com/dashboard?oauth_token=jkEaXJw1L1CjCCq3EuvW1evdQLONmMYh1TljLt7REw0OolFz33&oauth_verifier=UbAVlLW0gMkuZ1npqgAi37ZitsV4vFS804iCdmnJxw5RT0tMgX#_=_

# imports
from requests_oauthlib import OAuth1Session

request_token_url = "https://www.tumblr.com/oauth/request_token"
authorization_base_url = "https://www.tumblr.com/oauth/authorize"
access_token_url = "https://www.tumblr.com/oauth/access_token"

# get from console or file
input = input("Manual Input? [Y/n]: ")

# get control blog name
uuid = input("uuid: ")

# manual input
if (input == "" or input == "y"):

    # get manual input
    key = input("key: ")
    secret = input("secret: ")

# file input
elif (input == "n"):

    try:
        # open creds file
        creds_file = open(f"./../Credentials/{uuid}.txt", "r")

        uuid =          creds_file.readline()[:-1] # uuid on line one
        api_key =       creds_file.readline()[:-1] # api_key on line two
        api_secret =    creds_file.readline()[:-1] # api_secret on line three

        creds_file.close()
    
    # no target file
    except FileNotFoundError:
        print("Credentials File Not Found\nDefaulting to Manual Input")
        key = input("key: ")
        secret = input("secret: ")
    
# exit is called in the terminal
elif (input == "exit"):
    quit()

# something else entierly
else:
    quit()

# begin the authentication
# gotta play this by ear...

tumblr_login = OAuth1Session(client_key=api_key, client_secret=api_secret)
tumblr_login.fetch_request_token(request_token_url)
