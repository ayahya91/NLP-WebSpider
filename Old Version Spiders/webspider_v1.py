'''
	Web Spider Version 1: Failed. Build a V2
	Written By Ahmed Mused Yahya
'''

from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib import parse

# We are going to create a class called LinkParser that inherits some
# methods from HTMLParser which is why it is passed into the definition
class LinkParser(HTMLParser):
    # This is a function that HTMLParser normally has
    # but we are adding some functionality to it
    def __init__(self, URL):
    	self.links_to_visit = [URL]
    	self.baseUrl = URL
    	self.links_visited = []

    def handle_starttag(self, tag, attrs):
        # We are looking for the begining of a link. Links normally look
        # like <a href="www.someurl.com"></a>
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    # We are grabbing the new URL. We are also adding the
                    # base URL to it. For example:
                    # www.netinstructions.com is the base and
                    # somepage.html is the new URL (a relative URL)
                    #
                    # We combine a relative URL with the base URL to create
                    # an absolute URL like:
                    # www.netinstructions.com/somepage.html
                    newUrl = parse.urljoin(self.baseUrl, value)
                    print("Found URL, ", newUrl)
                    # And add it to our colection of links:
                    self.links_to_visit = self.links_to_visit + [newUrl]

    # This is a new function that we are creating to get links
    # that our spider() function will call
    def getLinks(self):
        # Remember the base URL which will be important when creating
        # absolute URLs
        url = self.NextLink()
        self.baseUrl = url
        # Use the urlopen function from the standard Python 3 library
        response = urlopen(url)
        # Make sure that we are looking at HTML and not other things that
        # are floating around on the internet (such as
        # JavaScript files, CSS, or .PDFs for example)
        self.VisitingLink()
        if response.getheader('Content-Type')=='text/html':
        	htmlBytes = response.read()
        	# Note that feed() handles Strings well, but not bytes
        	# (A change from Python 2.x to Python 3.x)
        	htmlString = htmlBytes.decode("utf-8")
        	self.feed(htmlString)
        	return htmlString, self.links_to_visit
        else:
            return "",[]

    def LinksToVisit(self):
    	return self.links_to_visit

    def NextLink(self):
        if self.links_to_visit != []:
            return self.links_to_visit[0]
        else:
            print("No more links")

    def VisitingLink(self):
    	self.links_visited = self.links_to_visit[0]
    	self.links_to_visit = self.links_to_visit[1:]
    	if self.links_to_visit == []:
        	print("No More Links Found!")

    def LinksCount(self):
    	return len(self.links_to_visit)

# And finally here is our spider. It takes in an URL, a word to find,
# and the number of pages to search through before giving up
def spider(url, word, maxPages):  
    pagesToVisit = [url]
    numberVisited = 0
    foundWord = False
    # The main loop. Create a LinkParser and get all the links on the page.
    # Also search the page for the word or string
    # In our getLinks function we return the web page
    # (this is useful for searching for the word)
    # and we return a set of links from that web page
    # (this is useful for where to go next)
    parser = LinkParser(url)
    while numberVisited < maxPages and parser.LinksCount != 0 and not foundWord:
        numberVisited = numberVisited +1
        # Start from the beginning of our collection of pages to visit:
        #try:
        print(numberVisited, "Visiting:", parser.NextLink())
        data, links = parser.getLinks()
        if data.find(word)>-1:
            foundWord = True
            # Add the pages that we visited to the end of our collection
            # of pages to visit:
            print(" **Success!**")           
        #except:
        #    print(" **Failed!**")

    if foundWord:
        print("The word", word, "was found at", url)
    else:
        print(" **Failed!**")
        print("Word never found. Number of Pages Visited: ", numberVisited)

spider("https://en.wikipedia.org/wiki/Cash", "physics", 200)