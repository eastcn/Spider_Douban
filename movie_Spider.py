"""
Name:spider of douban movie
Auther:east
2018/8/7
"""
import requests
from bs4 import BeautifulSoup as b

def get_web(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/60.0.3112.101 Safari/537.36'}
    r = requests.get(url, headers)
    soup = b(r.text, "html.parser")
    data = soup.find("ol",class_="grid_view")
    return data

def get_movie(data):
    info = data.find_all("li")
    for link in info:
        name = link.find("span",class_="title").get_text()
        other_name = link.find("span",class_="other").get_text().replace(' ','')
        score = link.find("span",class_="rating_num").get_text()
        try:
            remark = link.find("p",class_="quote").get_text().replace(' ','').replace('\n','')
        except:
            remark="暂无"
        with open("F:\\movie.txt","a+",encoding="utf-8") as f:
            f.write(name +" "+other_name+" "+score+" "+ remark + "\r\n" )
            print(name +" "+other_name+" "+score+" "+ remark + "\r\n")
if __name__ == '__main__':
    url = "https://movie.douban.com/top250"
    data=get_web(url)
    get_movie(data)





