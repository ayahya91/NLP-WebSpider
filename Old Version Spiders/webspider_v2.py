'''
	Web Spider Version 2: 
    Status: Fix So it subclasses htmlparser without overwriting it
	Written By Ahmed Mused Yahya

    Spider Object:
        mem_vars = [links_to_visit, links_visited, baseURL, current_word]
        mem_fun = [reset_spider, crawl, change_base_URL, handle_starttag, getLinks, LinksToVisit, NextLink, VisitingLink, LinksCount]
'''

from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib.parse import urlparse
from urllib.parse import urljoin
import os

class Spider(HTMLParser):
    def __init__(self, URL, word, maxpages=200):
        super(Spider, self).__init__()
        self.links_to_visit = [URL]
        self.baseUrl = urlparse(URL).netloc
        self.links_visited = []
        self.current_word = word
        self.num_links_visited = 0
        self.crawl(word, maxpages)
        self.spider_log = open(os.getcwd() + '/spider_log.txt', "a")

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    if "(" in value and ")" in value:
                        continue
                    elif urlparse(value).netloc != self.baseUrl and bool(urlparse(value).netloc):  # check if relative or absolute
                        newURL = value 
                    else:
                        print("Resolving ", self.links_to_visit[0], " ", urlparse(value).path)
                        newURL = urljoin(self.links_to_visit[0], urlparse(value).path)  #parse.urljoin(self.baseUrl, value)
                        print("To : ", newURL)
                    #print("Found URL, ", newURL)
                    self.links_to_visit = self.links_to_visit + [newURL]

    def getLinks(self):
        url = self.NextLink()
        if urlparse(url).netloc != self.baseUrl and bool(urlparse(url).netloc):     # change base url if visitng new host site
            print("Updating Spider.baseUrl from ", self.baseUrl, " to ", urlparse(url).netloc)
            self.baseUrl = urlparse(url).netloc
        response = urlopen(url)
        self.num_links_visited = self.num_links_visited + 1
        #if response.getheader('Content-Type')=='text/html':
        htmlBytes = response.read()
        htmlString = htmlBytes.decode("utf-8")
        #print ("HTML Data: \n", htmlString)
        self.feed(htmlString)
        self.VisitingLink()
        return htmlString
        #else:
        #    return ""

    def reset_spider(self, URL, word, maxpages=200):
        self.links_to_visit = [URL]
        self.baseUrl = URL
        self.links_visited = []
        self.current_word = word
        self.num_links_visited = 0
        self.crawl(word, maxpages)

    def change_base_URL(self, url=None, word=None, maxpages=200):
        # Retains Old Settings
        if url != None:
            self.baseUrl = [url]
        if word != None:
            self.current_word = word
        self.crawl(word, maxpages)

    def crawl(self, word, maxPages):  
        foundWord = False
        print("Crawling...")
        url = self.NextLink()
        while self.num_links_visited < maxPages and self.LinksCount != 0 and not foundWord:
            try:
                print(self.num_links_visited, "Visiting:", url)
                data = self.getLinks()
                if data.find(word)>-1:
                    foundWord = True
                    print(" **Success!** : Number of pages visited: ", self.num_links_visited)           
            except:
                print(" **Failed on URL: **", self.links_visited[-1])

        if foundWord:
            print("The word", word, "was found at", url)
            self.print_stats()
        else:
            print(" **Failed!**")
            print("Word never found. Number of Pages Visited: ", numberVisited)

    def LinksToVisit(self):
    	return self.links_to_visit

    def NextLink(self):
        if self.links_to_visit != []:
        	return self.links_to_visit[0]
        else:
            print("No more links")

    def VisitingLink(self):
    	self.links_visited = self.links_visited + [self.links_to_visit[0]]
    	self.links_to_visit = self.links_to_visit[1:]
    	if self.links_to_visit == []:
        	print("No Where Left To Crawl!")

    def LinksCount(self):
    	return len(self.links_to_visit)

    def LinksVisitedCount(self):
        return self.num_links_visited

    def print_stats(self):
        print("\n******************Spider Stats******************")
        print("------------------------------------------------")
        print("Spiders Current Word: ", self.current_word)
        print("Spiders Current Location:", self.links_visited[-1])
        print("Spider Depth: ", self.LinksVisitedCount())
        print("Spiders Links Left To Visit Count: ", self.LinksCount())
        response = raw_input("Press 'y' for listing, press anything else to quit: ")
        if response == 'y':
            print("Listed Below: \n",)
            for i in self.links_to_visit:
                print(i)
        print("------------------------------------------------")
        self.spider_log.close()

Spider(URL="http://www.tutorialspoint.com/ruby/ruby_operators.htm", word="Java ")