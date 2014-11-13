# -*- coding: utf-8 -*-
import urllib
import urllib2
import time
import json
from bs4 import BeautifulSoup

class pttCrawler():
    
    def __init__(self):
        self.startUrl = "https://www.ptt.cc/bbs/Gossiping/index.html"
        self.site = "https://www.ptt.cc"
        self.delay = 1
        self.allPosts = []
        self.opener = self.Opener()
        
    def Opener(self):
        cookies = urllib2.HTTPCookieProcessor()
        opener = urllib2.build_opener(cookies)
        data_encoded = urllib.urlencode({"from":"/bbs/Gossiping/index.html","yes":"yes"})
        opener.open("https://www.ptt.cc/ask/over18",data_encoded)
        return opener
    
    def Active(self):
        soup = self.getSoup(self.startUrl)
        ACTIVE = True
        
        while ACTIVE:
            self.getPost(soup)
            plink = self.getPrevPage(soup)
            soup = self.getSoup(plink)
        
        
    def getPrevPage(self, soup):
        btnGroup = soup.body.find_all('a', class_='btn wide')
        for btn in btnGroup:
            if u"上頁" in btn.string:
                return self.site + btn['href']
        
    def getSoup(self, url):
        srcPage = self.opener.open(url)
        return BeautifulSoup(srcPage)
    
    def getPost(self, soup):
        tmp_posts = soup.body.find_all('div', class_='r-ent')
        tmp_posts_buffer = []
        
        for tmp_post in tmp_posts:
            # Check <a>
            if tmp_post.a is None:
                continue
            # Check post exists
            for post in self.allPosts:
                # If exists
                if self.site + tmp_post.a['href'] == post['href']:
                    # Update nrec
                    if tmp_post.span is not None:
                        post['nrec'] = tmp_post.span.string
                        break
                    else:
                        post['nrec'] = u'0'
                        break
            
            # Generate Dictionary
            post_data = {}
            post_data['title'] = tmp_post.a.string
            post_data['href'] = self.site + tmp_post.a['href']
            post_data['date'] = tmp_post.find('div', class_='date').string
            post_data['author'] = tmp_post.find('div', class_='author').string
            if tmp_post.span is not None:
                post_data['nrec'] = tmp_post.span.string
            else:
                post_data['nrec'] = u'0'
            # Reverse posts
            tmp_posts_buffer.append(post_data)
        
        self.allPosts.extend(tmp_posts_buffer[::-1])
        for data in tmp_posts_buffer[::-1]:
            print data['date'] + '-' + data['title'] + '-' + data['author']
    
    def mkjson(self):
        f = open('posts.json', 'w+')
        json.dump(self.allPosts, f)
        f.close()
    
