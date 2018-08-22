from urllib.request import urlopen
from bs4 import BeautifulSoup

URL= 'http://www.pythonscraping.com/pages/page3.html'
html = urlopen(URL)
bsObj = BeautifulSoup(html)

for child in bsObj.find('table',{'id':'giftList'}).children:
    print(child)

