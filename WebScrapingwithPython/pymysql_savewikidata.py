from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random
import pymysql

conn = pymysql.connect(host = '127.0.0.1',)

cur = conn.cursor()
cur.execute('USE scraping')
random.seed(datetime.datetime.now())

def store(title,content):
    cur.execute()
    cur.connection.commit()

def getLinks(articleUrl):
    html = urlopen('http://')
    bsObj = BeautifulSoup(html)
    title = bsObj.find('h1').get_text()
    content = bsObj.find('dev',)
    store(title,content)
    return bsObj.find('div',)

links = getLinks('')

try:
    while len(links)>0:
        newArticle = links[random.randint(0,len(links))]
        print(newArticle)
        links = getLinks(newArticle)

finally:
    cur.close()
    conn.close()
    