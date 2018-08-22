#解析codewars排行榜网页数据
from bs4 import BeautifulSoup
from urllib.request import urlopen
URL = 'https://www.codewars.com/users/leaderboard'

def solution():
    html = urlopen(URL)
    bsObj = BeautifulSoup(html)
    position = []
    for tr in bsObj.findAll('tr'):
        pos_i = []
        for td in tr:
            pos_i.append(td.get_text())
        pos_i.remove(pos_i[0])
        pos_i[0] = pos_i[0][5:]
        print(pos_i)
        position.append(pos_i)
    del position[0]
    return position

a = solution()
print(a)


#tips：list添加数据为二维数组：
#book_list.append([title,rating,people_num,author_info,pub_info])