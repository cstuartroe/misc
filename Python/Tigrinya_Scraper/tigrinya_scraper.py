from bs4 import BeautifulSoup as bs
import urllib.request as ur
import lxml

with ur.urlopen(input('site address: ')) as response:
    raw_html = response.read()

stew = bs(raw_html,'lxml')

def analyze_goethe(stew):
    tigs = stew.find_all('div',style='display:none')
    return [tig.a.contents[0].strip()+'\n' for tig in tigs]

def english_goethe(stew):
    tigs = stew.find_all('div',{'class':'Stil35'})
    return [tig.text.strip() + '\n' for tig in tigs]

tigs = analyze_goethe(stew)
with open('scraper_out.txt','w',encoding='utf-8') as fh:
     fh.writelines(tigs)

engs = english_goethe(stew)
with open('scraper_eng.txt','w',encoding='utf-8') as fh:
     fh.writelines(engs)
