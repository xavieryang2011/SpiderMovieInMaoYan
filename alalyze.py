import csv

time = []
nickName = []
gendar = []
cityName = []
score = []
content = ''

#读数据
def read_csv():
	content = ''
	with open(r'wushuang.csv','r',encoding='utf_8_sig',newline='') as file_test:
		reader = csv.reader(file_test)
		i = 0
		for row in reader:
			if i != 0:
				cityName.append(row[0])
				content += row[1]
				nickName.append(row[2])
				gendar.append(row[3])
				score.append(row[4])
				time.append(row[5])
			i = i+1
		print("一共有"+str(i)+"个")
		return content

import re,jieba
#词云生成工具
from wordcloud import WordCloud,ImageColorGenerator
#需要对中文进行处理
import matplotlib.font_manager as fm
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
from os import path

d = path.dirname(__file__)
stopwords_path = d+'/static/stopword.txt'

#评论词云分析
def word_cloud(content):
	import jieba,re,numpy
	from pyecharts import WordCloud
	import pandas as pd

	#去除评论所有多余字符
	content = content.replace(" ",",")
	content = content.replace(" ","、")
	content = re.sub('[,,。.\r\n]','',content)

	segment = jieba.lcut(content)
	words_df = pd.DataFrame({'segment':segment})
	#quoting=3表示stopword.txt里的内容不引用
	stopwords = pd.read_csv(stopwords_path,index_col=False,quoting=3,sep="\t",names=['stopword'],encoding='utf_8')
	words_df = words_df[~words_df.segment.isin(stopwords.stopword)]
	words_stat = words_df.groupby(by=['segment'])['segment'].agg({'计数':numpy.size})
	words_stat = words_stat.reset_index().sort_values(by=["计数"],ascending=False)
	test = words_stat.head(500).values
	codes = [test[i][0] for i in range(0,len(test))]
	counts = [test[i][1] for i in range(0,len(test))]
	wordcloud = WordCloud(width=1300,height=620)
	wordcloud.add('影评词云',codes,counts,word_size_range=[20,100])
	wordcloud.render('word_cloud_wushuang.html') 

	#评论城市可视化
def city_table(cityName):
		print(cityName)
		cityList=list(set(cityName))
		city_dict = {cityList[i]:0 for i in range(len(cityList))}
		for i in range(len(cityList)):
			city_dict[cityList[i]] = cityName.count(cityList[i])
		sort_dict = sorted(city_dict.items(),key=lambda d:d[1],reverse=True)
		city_name = []
		city_num = []
		for i in range(len(sort_dict)):
			city_name.append(sort_dict[i][0])
			city_num.append(sort_dict[i][1])
		
		import random
		from pyecharts import Bar
		bar = Bar('评论者城市分布')
		bar.add("",city_name,city_num,is_label_show=True,is_datazoom_show=True)
		bar.render(d+'/picture/city_bar.html')

def make_word_cloud(content):
	content = content.replace('无双','')
	bg = plt.imread(d + r'/static/znn.jpg')
	#生成
	wc = WordCloud(
		background_color='white',
		width = 890,
		height=600,
		mask=bg,
		max_font_size=150,
		random_state=50,
		font_path=d+"/static/simkai.ttf").generate_from_text(content)
	#为图片设置字体
	myfont = fm.FontProperties(fname=d+'static/simkai.ttf')
	bg_color = ImageColorGenerator(bg)
	#开始画图
	plt.imshow(wc.recolor(color_func=bg_color))
	#为云图去掉坐标轴
	plt.axis('off')
	wc.to_file(d+'/picture/wc_cloud_c.png')
	pass

time = []
nickName = []
gendar = []
cityName = []
score = []
content = ''
#词云图
content = read_csv()
# word_cloud(content)

#城市分布
# city_table(cityName)
#云图
make_word_cloud(content)