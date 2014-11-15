# -*- coding: utf-8 -*-
import os
import urllib
import urllib2
import time
import json
import datetime
from collections import OrderedDict
from bs4 import BeautifulSoup
from settings import *

class pttCrawler():

    def __init__(self):
        #self.posts = {}
        self.posts = OrderedDict([])
        self.Opener()
        self.makeDir()

    def readback(self):
        pass

    def travel(self, url):
        # Travel website one time.
        # self.posts.update(self.getPost(self.getSoup(url)))
        pass

    def update(self):
        # Update init
        soup = self.getSoup(START_URL)
        endDate = self.getEndDate(DAY_CYCLE)

        # update loop
        while True:
            posts = self.getPost(soup)
            for date, data in posts.iteritems():
                if date not in self.posts.keys():
                    self.posts.setdefault(date, OrderedDict([]))
                self.posts[date].update(data)

            plink = self.getPrev(soup)
            soup = self.getSoup(plink)

            if endDate in self.posts.keys():
                break

    def Opener(self):
        cookies = urllib2.HTTPCookieProcessor()
        opener = urllib2.build_opener(cookies)
        data_encoded = urllib.urlencode({"from":"/bbs/Gossiping/index.html","yes":"yes"})
        opener.open(OVER18, data_encoded)
        self.opener = opener
        return opener

    def getSoup(self, url):
        while True:
            try:
                srcPage = self.opener.open(url)
            except urllib2.URLError:
                print("Operation Time out")
            break

        return BeautifulSoup(srcPage)

    def getPost(self, soup):
        # Get Posts from a soup object, and return a dictionary of these posts.

        tmpPosts = soup.body.find_all('div', class_='r-ent')
        tmpPosts.reverse()
        #tmpPostsBuf = {}
        tmpPostsBuf = OrderedDict([])

        for tmpPost in tmpPosts:
            try:
                # A Single Post
                date = tmpPost.find('div', class_='date').string
                href = tmpPost.a['href']
                title = tmpPost.a.string
                author = tmpPost.find('div', class_='author').string
                if tmpPost.span is None:
                    nrec = u'0'
                else:
                    nrec = tmpPost.span.string

                # Save posts to buffer
                if date not in tmpPostsBuf.keys():
                    tmpPostsBuf.setdefault(date, OrderedDict([]))
                tmpPostsBuf[date][href] = (title, author, nrec)

            except TypeError as e:
                print "TypeError! Continue..."
                continue

        # Print the data already been crawled
        for key1, value1 in tmpPostsBuf.iteritems():
            for key2, value2 in value1.iteritems():
                print '[' + key1 + ']' + value2[0] + '-' + value2[1]

        return tmpPostsBuf

    def mkJson(self):
        for date, data2 in self.posts.iteritems():
            json_list = []
            for href, data1 in data2.iteritems():
                post = {}
                post['title'] = data1[0]
                post['author'] = data1[1]
                post['nrec'] = data1[2]
                post['date'] = date
                post['href'] = SITE + href
                json_list.append(post)
            fileName = os.path.join(SAVE_PATH, date[:2] + '-' + date[3:] + '-' + '2014')
            with open(fileName, 'w') as file:
                json.dump(json_list, file)

    def getPrev(self, soup):
        btnGroup = soup.body.find_all('a', class_='btn wide')
        for btn in btnGroup:
            if u"上頁" in btn.string:
                return SITE + btn['href']

    def getCurDate(self):
        if time.localtime().tm_mday in [day for day in range(1,10)]:
            return str(time.localtime().tm_mon) + '/' + '0' + str(time.localtime().tm_mday)
        else:
            return str(time.localtime().tm_mon) + '/' + str(time.localtime().tm_mday)

    def getEndDate(self, endDays):
        Date = datetime.datetime.strptime(self.getCurDate(), "%m/%d")
        EndDate = Date - datetime.timedelta(days=endDays)
        if EndDate.day in [day for day in range(1,10)]:
            return str(EndDate.month) + '/' + '0' + str(EndDate.day)
        else:
            return str(EndDate.month) + '/' + str(EndDate.day)

    def makeDir(self):
        if not os.path.isdir(SAVE_PATH):
            os.makedirs(SAVE_PATH)
