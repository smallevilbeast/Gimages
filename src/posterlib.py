import os
import sys
import urllib
import urllib2
import urlparse
import re
import cookielib
import time
    
import socket    
socket.setdefaulttimeout(40) # 40s

import utils
from logger import Logger

class Poster(Logger):
    
    def __init__(self):
        cookie_file = utils.get_cookie_file()
        cj = cookielib.LWPCookieJar(cookie_file)
        cookie_handler = urllib2.HTTPCookieProcessor(cj)
        opener = urllib2.build_opener(cookie_handler)
        opener.addheaders = [
            ('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.24 ' \
             '(KHTML, like Gecko) Chrome/19.0.1056.0 Safari/535.24'),]
        self.cookiejar = cj
        if os.path.isfile(cookie_file):
            self.cookiejar.load(ignore_discard=True, ignore_expires=True)
        self.opener = opener
        
        self.apidata = {}
        
    def api_request(self, api, method="GET", extra_data=dict(), retry_limit=2, encoding=None, **params):    
        url = urlparse.urljoin("http://images.google.com.hk", api)
        data = self.apidata.copy()
        data.update(extra_data)
        data.update(params)
        for key in data:
            if callable(data[key]):
                data[key] = data[key]()
            if isinstance(data[key], (list, tuple, set)):
                data[key] = ",".join(map(str, list(data[key])))
            if isinstance(data[key], unicode):    
                data[key] = data[key].encode("utf-8")
                
        if method == "GET":        
            if data:
                query = urllib.urlencode(data)
                url = "%s?%s" % (url, query)
            req = urllib2.Request(url)
        elif method == "POST":
            body = urllib.urlencode(data)
            req = urllib2.Request(url, data=body)
            
        self.logdebug("API request url: %s", url)    
        start = time.time()    
        try:
            ret = self.opener.open(req)
        except Exception, e:    
            if retry_limit == 0:
                self.logdebug("API request error: url=%s error=%s",  url, e)
                return dict(result="network_error")
            else:
                retry_limit -= 1
                return self.api_request(api, method, extra_data, retry_limit, **params)
            
        if encoding is None:    
            raw = ret.read()
        else:    
            try:
                raw = ret.read().decode(encoding)
            except:    
                raw = ret.read()
                
        self.logdebug("API response %s TT=%.3fs", api, time.time() - start )
        return raw                
    
    def query_image(self, name):
        params = {"q" : name, "hl" : "zh-CN", "safe" : "strict", "biw" : "1366",
                  "bih" : "647", "site": "imghp", "tbs" : "isz:ex,iszw:48,iszh:48",
                  "tbm" : "isch", "source": "lnt", "sa": "X",
                  "ei": "06eXUJL3EuT3mAWBs4CgDA", "ved": "0CCQQpwUoBQ"}
        
        return self.filter_image(self.api_request("search", "GET", extra_data=params))
        
        
    def filter_image(self, html):    
        url_pattern  = re.compile(r'ltq\":\"(.*?)\"')
        urls = url_pattern.findall(html)
        if urls:
            return urls[0]
        return None
        
if __name__ == "__main__":        
    poster = Poster()
    poster.query_image("amarok")
