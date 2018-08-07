"""
Name:spider of douban book
Auther:east
2018/8/6
"""

from urllib import request as r
from bs4 import BeautifulSoup

def get_html(url):
    html = r.urlopen(url)
    soup = BeautifulSoup(html,"html.parser")
    data = soup.find("div",id="wrapper") # wrapper是整个图书栏的div
    return data

def get_data(data):
    table=data.find_all('table')
    for link in table:
        name = link.find("div",class_="pl2").find('a').get_text().replace(' ','').replace('\n','')  # id=p12 中是书名所在， 这里暂时没用过滤空格
        author = link.find('p',class_="pl").get_text().split('/')[0].replace(' ','')  #只获取作者
        time = link.find('p',class_="pl").get_text().split('/')[-2].replace(' ','')  #获取出版时间
        score = link.find('span',class_='rating_nums').get_text().replace(' ','')  #class 为python默认的方法所以需要加下划线加以区别
        people_num = link.find('span',class_='pl').get_text().replace(' ','').replace('(','').replace(')','').replace('\n','')
        print(name+author+time+score+people_num)
        with open('F://book.txt', 'a+', encoding='UTF-8') as f:
            f.write(name + ' ' + author + ' ' + time + ' ' + score + ' ' + people_num + ' ' + '\r\n')



if __name__ == '__main__':
    url='https://book.douban.com/top250?start='
    with open('F://book.txt','a+',encoding='utf-8') as f:
        f.write('书籍名称 '+'作者 '+'出版时间'+'评分 '+'评价人数 '+'\r\n')
    for i in range(10):
        url1 = url + str(i * 25)
        get_data(get_html(url1))




