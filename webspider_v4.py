'''
	Web Spider Version 3: 
    Status: Functional
	Written By Ahmed Mused Yahya

    Spider Object:
        mem_vars = [wait_queue, links_visited, baseURL, current_word]
        mem_fun = [reset_spider, crawl, change_base_URL, handle_starttag, readPage, VisitingLink, LinksCount]
'''
'''!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    !!!! Use NLTK/machine learning to learn a topic, search the web and find information (web pages), to send to you for brainstorming.!!!!
    !!!! Think Search Engine but you don't even have to input a query. Just a topic. !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'''


from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib.parse import urlparse
from urllib.parse import urljoin
import os, sys, datetime, time

class Spider(HTMLParser):
    def __init__(self, URL, phrase, maxpages=200):
        super(Spider, self).__init__()
        self.wait_queue = None 
        self.baseUrl = None
        self.search_phrase = None
        self.search_span = 0
        input_test = self.change_base_URL(URL, phrase, maxpages)
        if input_test != 0:
        	print("Invalid Input Parameters.")
        	return
        self.spider_log = open(os.getcwd() + "/Spider Logs/spiderlog_" + str(datetime.datetime.today()) + ".txt", "w")
        self.links_visited = []
        self.num_links_visited = 0
        start_time = time.time()
        self.crawl()
        self.execution_time = time.time() - start_time
        self.Write_Stats()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    if "(" in value and ")" in value:
                        continue
                    elif urlparse(value).netloc != self.baseUrl and bool(urlparse(value).netloc):  # check if relative or absolute
                        newURL = value
                        print("Found New URL: " + newURL + ".\n")
                        self.spider_log.write("Found New URL: " + newURL + ".\n")
                    else:
                        #newURL = urljoin(self.baseUrl, urlparse(value).path)  #parse.urljoin(self.baseUrl, value)
                        newURL = self.baseUrl + urlparse(value).path
                        print("Found New URL: Resolving " + self.wait_queue[0] + " " + urlparse(value).path + "To : " + newURL + ".\n")
                        self.spider_log.write("Found New URL: Resolving " + self.wait_queue[0] + " " + urlparse(value).path + "To : " + newURL + ".\n")
                    if self.check_visit_status(newURL): 
                        #Make sure URL is formatted correctly
                        newURL = newURL.replace("**", "")
                        newURL = newURL.replace("../", "/")
                        self.wait_queue = self.wait_queue + [newURL]

    def check_visit_status(self, newURL):
        if newURL not in self.wait_queue and newURL not in self.links_visited:
            return True
        else:
            return False

    def reset_spider(self, URL, word, maxpages=200):
        input_test = self.change_base_URL(URL, phrase, maxpages)
        if input_test != 0:
        	print("Invalid Input Parameters.")
        	return
        self.links_visited = []
        self.num_links_visited = 0
        self.spider_log = open(os.getcwd() + "/Spider Logs/spiderlog_" + str(datetime.datetime.today()) + ".txt", "w")
        start_time = time.time()
        self.crawl(self.search_phrase, self.search_span)
        self.execution_time = time.time() - start_time
        self.Write_Stats()

    def change_base_URL(self, url=None, phrase=None, maxpages=200, grep_options=""):
        # Retains Old Settings
        if url != None and isinstance(url,str) and bool(urlparse(url).netloc):
            self.wait_queue = [url]
            self.baseUrl = urlparse(url).netloc
        else:
        	print(url + " is not a valid URL.")
        	return -1
        if phrase != None and isinstance(url,str):
            self.search_phrase = phrase
        else:
        	print("Please specify a word.")
        	return -2
        if isinstance(maxpages, int) and maxpages > 0:
        	self.search_span = maxpages
       	else:
       		print("Max pages must be greater than 0.")
        	return -3
        return 0

    def readPage(self):
        url = self.wait_queue[0]
        if  bool(urlparse(url).netloc) and urlparse(url).netloc != self.baseUrl:     # change base url if visitng new host site
            print("Updating Spider.baseUrl from " + self.baseUrl + " to " + urlparse(url).netloc + ".\n")
            self.spider_log.write("Updating Spider.baseUrl from " + self.baseUrl + " to " + urlparse(url).netloc + ".\n")
            self.baseUrl = urlparse(url).netloc
        try:
            response = urlopen(url)
            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")
            self.feed(htmlString)
            #print("HTML Data " + htmlString)
        except (urllib.error.HTTPError, NameError) as e:
            self.spider_log.write("Exception: " + str(e) + ".\n")
            print("Nothing there...")
        except:
            self.spider_log.write("Exception: Other Exception: " + str(sys.exc_info()[0]) + ".\n")

        self.num_links_visited = self.num_links_visited + 1                 #if response.getheader('Content-Type')=='text/html':
        self.VisitingLink()
        return htmlString

    def crawl(self):  
        foundWord = False
        self.spider_log.write("Crawling...\n")
        print("Crawling...\n")
        while self.num_links_visited < self.search_span and self.LinksCount != 0 and not foundWord:
            try:
                url = self.wait_queue[0]
                print(str(self.num_links_visited) + " Visiting:" + self.wait_queue[0] + ".\n")
                data = self.readPage()
                if data.find(self.search_phrase)>-1:
                    foundWord = True
                    print("**Success!** : Number of pages visited: " + self.num_links_visited + ".\n") 
                    self.spider_log.write("**Success!** : Number of pages visited: " + self.num_links_visited + ".\n")      
            except (NameError) as e:
                self.spider_log.write("Exception: " + str(e) + ".\n")
            except:
                print("**Failed on URL: **" + url + ".\n")
                self.spider_log.write("**Failed on URL: **" + url + " Exception : " + str(sys.exc_info()[0]) + ".\n")
            
            if url == self.wait_queue[0]:
                self.VisitingLink()                 # last link was not removed from queue, remove it

        if foundWord:
            print("The word " + self.search_phrase + " was found at " + url + ".\n")
            self.spider_log.write("The word " + self.search_phrase + " was found at " + url + ".\n")

        else:
            print("**Failed!**.\n")
            print("Word never found. Number of Pages Visited: " + str(self.num_links_visited) + ".\n")
            self.spider_log.write("**Failed!**.\n")
            self.spider_log.write("Word never found. Number of Pages Visited: " + str(self.num_links_visited) + ".\n")

    def VisitingLink(self):
    	self.links_visited = self.links_visited + [self.wait_queue[0]]
    	self.wait_queue = self.wait_queue[1:]
    	if self.wait_queue == []:
            print("No Where Left To Crawl!.\n")
            self.spider_log.write("No Where Left To Crawl!.\n")
            sys.exit()

    def LinksCount(self):
    	return len(self.wait_queue)

    def LinksVisitedCount(self):
        return self.num_links_visited

    def Write_Stats(self):
        self.spider_log.write("\n******************Spider Stats******************.\n")
        self.spider_log.write("------------------------------------------------.\n")
        self.spider_log.write("Spider Execution Time: " + str(self.execution_time) + " seconds.\n")
        self.spider_log.write("Spiders Current Word: " + self.search_phrase + ".\n")
        self.spider_log.write("Spiders Current Location: " + self.links_visited[-1] + ".\n")
        self.spider_log.write("Spider Depth: " + str(self.LinksVisitedCount()) + ".\n")
        self.spider_log.write("Spiders Links Left To Visit Count: " + str(self.LinksCount()) + ".\n")
        self.spider_log.write("------------------------------------------------\n")
        self.spider_log.write("Links Left To Visit:\n")
        for i in self.wait_queue:
            self.spider_log.write(i + ".\n")
        self.spider_log.write("------------------------------------------------\n")
        self.spider_log.close()

#Spider(URL=sys.argv[1], phrase=sys.argv[2])
