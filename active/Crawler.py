from Own import Own
from Blog import Blog
from User import User
from Security import Security
from requests_oauthlib import OAuth1
import datetime
import threading

sec = Security("botbreaker")

class Crawler:
        
    # constructors for Crawler
    # first time
    def __init__(self, security="", lead_bot_name="CRAWLER"):

        self.lead_bot_name = lead_bot_name

        self.uuid, self.api_key, self.api_secret, self.oauth_key, self.oauth_secret = security.getDetails()

        self.oauth = OAuth1(client_key=self.api_key,
                            client_secret=self.api_secret,
                            resource_owner_key=self.oauth_key,
                            resource_owner_secret=self.oauth_secret)

        # all requests start thus
        self.base_url = "https://api.tumblr.com/v2/user/"
        
        self.blog = Blog(self.uuid, self.api_key, self.api_secret, self.oauth_key, self.oauth_secret)
        self.user = User(self.uuid, self.api_key, self.api_secret, self.oauth_key, self.oauth_secret)
        self.own = Own(self.uuid, self.api_key, self.api_secret, self.oauth_key, self.oauth_secret)

        
        self.logs = {"lead_bot" : lead_bot_name,
                     "logs" : {},
                     "blog_trail" : [self.uuid]}
        
        print(self.logs)
        

    def crawler(self, target_blog_name, version):
        try:
            own = self.own

            sub_log = {"target_blog" : target_blog_name,
                       "version" : version,
                       "timestamp" : str(datetime.datetime.utcnow().isoformat())}

            following_list = own.bulkList(target_blog=target_blog_name, target_type="blog following")
            following_list_names = own.getAttributeList(following_list, "name")
            
            sub_log['blogs'] = following_list_names
            self.logs['blog_trail'] = following_list_names

            i = 0
            bot_threads = []
            for name in following_list_names:
                current_version = str(version)+"."+str(i)

                if not name in self.logs['blog_trail']:
                    bot_threads.append(threading.Thread(target=self.crawler, args=(name, current_version,)))

                i += 1

            for thread in bot_threads:
                thread.start()

            i = 0
            for thread in bot_threads:
                bot_threads[len(bot_threads) - (i+1)].join()



            self.logs['logs'][version] = sub_log

        except KeyError:
            self.logs['logs'][version] = "LOCKED"
            # print(self.logs)

        return self.logs



crawler = Crawler("CRAWLER", sec)

crawler_report = crawler.crawler("botbreaker", 1)
crawler_logs = crawler_report['logs']

i = 0
for log in crawler_logs:
    print(crawler_logs[log])
    i+=1
