"""
Name:spider of douban book
Auther:east
2018/8/6
"""
import requests
import jieba
import re
import numpy
import pandas
from bs4 import BeautifulSoup as B
from wordcloud import WordCloud
import matplotlib.pyplot as plt

#爬去评论
def get_comment(movieid):
	pagenum = 25
	comment_list = []
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/60.0.3112.101 Safari/537.36'}
	for i in range(pagenum):
		start = i * 20
		url = ("https://movie.douban.com/subject/" + movieid + "/comments"+"?" + "start=" + str(start) + "&limit=20"+"status=P")
		r = requests.get(url,headers)
		websoup = B(r.text,"html.parser")
		div_list = websoup.find("div",id="wrapper").find_all('div',class_="comment")
		for link in div_list:
			comment_name =link.find("a",class_="").get_text()
			comment = link.find("span",class_="short").get_text().replace(' ','').replace('\n','')
			vote = link.find("span",class_="votes").get_text()
			comment_list.append(comment)
			with open('D:\\python_study\\Spider_Douban\\comment.txt','a+',encoding="utf-8") as f:
				f.write(comment_name+": "+ comment + " " + vote + "\r\n")
	return comment_list

#过滤字段
def filter_(comment_list):
	comment = ""
	for i in comment_list:
		comment = comment + i
	# 去除标点的正则
	filter_rate = re.compile(r"[^\u4E00-\u9FA5]")
	comment_filter= filter_rate.sub(r"",comment)

	# for i in comment_list:
	# 	filter_str = filter_rate.sub(r"",comment_list[i])
	# 	comment_filter_list.append(filter_str)

	#结巴分词
	segment = jieba.lcut(comment_filter)
	words_df = pandas.DataFrame({"segment":segment})

	#stop words
	stopword=pandas.read_csv(
		"./stopwords.txt",
		index_col=False,
		quoting=3,
		sep="t",
		names=["stopword"],
		encoding="utf-8"
	)
	words_df =words_df[~words_df.segment.isin(stopword.stopword)]

	return words_df

#生成图
def statistics(words_df,moviename):
	words_stat = words_df.groupby (by=["segment"]) ["segment"].agg ({"计数": numpy.size})
	words_stat = words_stat.reset_index ().sort_values (by=["计数"], ascending=False)
	print (words_stat)
	wordcloud = WordCloud(
        font_path="‪C:\\Windows\\Fonts\\msyh.ttc",
        background_color="white",
        max_font_size=150,
        width=1000,
        height=860,
        margin=2,
    )
	word_frequence = {x [0]: x [1] for x in words_stat.head (500).values}
	wordcloud = wordcloud.fit_words (word_frequence)
	plt.imshow (wordcloud)
	plt.axis ("off")
	plt.show (block=False)
	img_name = "./" + moviename + ".jpg"
	wordcloud.to_file (img_name)

if __name__ == "__main__":
	movieid=str(27622447)
	moviename="小偷家族"
	#print(get_comment(movieid))
	statistics(filter_(get_comment (movieid)),moviename)




