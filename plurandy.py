import re
from bs4 import BeautifulSoup as bs
from urllib import request as ur

global page_queue
page_queue = []

def repeat_capture(pattern,s,flags=None): # it's dumb that python doesn't do this
    out = []
    searching = True
    while searching:
        x = re.search(pattern, s, flags)
        if x is None:
            searching = False
        else:
            out.append(re.search("match='(.*)'",str(x)).groups(0)[0].strip())
            s = s[x.span()[1]:]
    return out

def plurandy(s):
    return repeat_capture("([plurandy]{3,} ?)+", s,flags=re.I)

def scrape_plurandy(start,demise=3):
    global page_queue
    soup = bs(ur.urlopen(start).read(),"html5lib")
    page_queue += [a.get("href","") for a in soup.find_all("a")]
    for name in plurandy(soup.text):
        print(name)

x = scrape_plurandy("https://www.npr.org/")
