import urllib
from urllib.parse import urlparse, parse_qs, urlunparse, urlsplit
from bs4 import BeautifulSoup
from datetime import datetime
import sys
import re

#a random thread starter
url = sys.argv[1]

class Post:
    
    regex = re.compile("/images/sp.\.gif")
    
    def __init__(self, url):
        self.url = url
        self.parsed_url = urlparse(url)
        self.forum_id = None
        self.message_id = None
        self.author = None
        self.content = None
        self.title = None
        self.time = None
        self.children = []
        
    #process the URL and turn it into soup
    def make_soup(self):
        my_url = self.url
        req = urllib.request.Request(my_url)
        response = urllib.request.urlopen(req)
        thePage = response.read()
        return BeautifulSoup(thePage, 'lxml')

    '''grab post data'''
    def fill_post(self):
        #pull in data
        my_soup = self.make_soup()
        
        
        #get forum_id
        query = parse_qs(self.parsed_url.query)
        self.forum_id = query['forumid'][0]
        self.message_id = int(query['messageid'][0])

        #get title
        self.title = my_soup.find('title').get_text()

        #get content
        self.content = my_soup.find(class_ = 'ForumText').get_text()

        #get author.  There are multiple <b>, but the first is the author
        self.author = my_soup.find('b').get_text()

        #get timestamp
        my_time = my_soup.find('em').get_text()
        my_time = my_time.strip(' ')
        my_time_real = datetime.strptime(my_time, '%m/%d/%y %I:%M%p')
        self.time = datetime.strftime(my_time_real, '%Y-%m-%d %H:%M:00')
        
        #bring in children
        self.rest_of_thread(my_soup)

    '''all other posts in this thread'''        
    def rest_of_thread(self, my_soup):
        #TDAlt9 is unique for the messages table, specifically a cell in it
        t = my_soup.find(class_ = 'TDAlt9')
        thread_table = t.parent.parent
        for r in thread_table.find_all('tr'):
            i = r.find('img')
            try:   #first row has no image
                if re.match('/images/sp.\.gif', i['src']):   #children are sp1, grandchildren sp2, etc
                    ra = r.find('a', class_='A2')     #profiles have links, but not A2 class
                    rah = ra['href']
                    parsed_rah = urlparse(rah)
                    rah_query = parse_qs(parsed_rah.query)
                    self.children.append(tuple((rah_query['forumid'][0], rah_query['messageid'][0])))
            except:
                continue

    '''print for validation'''
    def display(self):
        print(self.author + ' @ ' + self.time)
        print('==='+self.title+'===')
        print(self.content)
        print('')

def display_thread(my_post):
    my_post.display()
    try:
        for c in my_post.children:
            my_query = 'forumid=%s&messageid=%s&action=view&format=threaded' % c
            my_url = urlunparse((my_post.parsed_url.scheme, my_post.parsed_url.netloc, my_post.parsed_url.path, '', my_query, ''))
            my_child = Post(my_url)
            my_child.fill_post()
            my_child.display()
    except:
        print('none')

a_post = Post(url)
a_post.fill_post()

display_thread(a_post)