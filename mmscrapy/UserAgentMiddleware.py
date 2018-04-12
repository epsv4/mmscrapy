import random  
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware  
  
class RotateUserAgentMiddleware(UserAgentMiddleware):  
    def __init__(self, user_agent=''):  
        self.user_agent = user_agent  
  
    def process_request(self, request, spider):  
        ua = random.choice(self.user_agent_list)  
        if ua:  
            print ua, '-----------------yyyyyyyyyyyyyyyyyyyyyyyyy'  
            request.headers.setdefault('User-Agent', ua)  
  
    #the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape  
    #for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php  
    user_agent_list = [
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
       ]  