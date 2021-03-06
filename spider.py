import requests,time
from fake_useragent import UserAgent
import json,csv,os
import pandas as pd

class Spider_maoyan():
	"""docstring for spiderMaoYan"""
	headers = {
	     "User-Agent": UserAgent(verify_ssl=False).random,
	     "Host": "m.maoyan.com",
	     "Referer": "http://m.maoyan.com/movie/342166/comments?_v_=yes"
	}
	def __init__(self, url,time):
		self.url = url
		self.time = time

	def get_json(self):
		# 发送get请求
		response_comment = requests.get(self.url, headers=self.headers)
		json_comment = response_comment.text
		json_comment = json.loads(json_comment)
		print(self.url)
		return json_comment

	def getData(self,json_comment):
		json_response = json_comment["cmts"]
		listinfo = []
		for data in json_response:
			cityName = data["cityName"]
			content = data["content"]
			nick = data["nick"]
			if "gender" in data:
			    gender = data["gender"]
			else:
				gender = 0
			score = data["score"]
			watchtime = data["time"]
			listone = [cityName,content,nick,gender,score,watchtime]
			listinfo.append(listone) 
			pass
		self.file_do(listinfo)
		pass

	def file_do(self,listinfo):
		file_size = os.path.getsize(r'wushuang.csv')
		if file_size == 0:
			name = ['城市','评论','昵称','性别','评分','观影时间']
			file_test = pd.DataFrame(columns=name,data=listinfo) 
			file_test.to_csv(r'wushuang.csv',encoding='utf_8_sig',index=False)
		else:
			with open(r'wushuang.csv','a+',encoding='utf_8_sig',newline='') as file_test:
				writer = csv.writer(file_test)
				writer.writerows(listinfo)
		pass

def spider_maoyan():
	# 猫眼电影短评接口
	offset = 0
	# 电影是2018.9.21上映的
	startTime = '2018-10-01'
	day = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
	j = 0
	page_num = int(20000/15)
	for i in range(page_num):
		print(i)
		comment_api = 'http://m.maoyan.com/mmdb/comments/movie/342166.json?_v_=yes&offset={0}&startTime={1}%2011%3A31%3A51'.format(offset,startTime)
		s0 = Spider_maoyan(comment_api,startTime)
		json_comment = s0.get_json()
		if json_comment["total"] == 0: # 当前时间内评论爬取完成
			if j < 16:
				startTime = '2018-10-%d'%day[j]
			else: # 全部爬完
				break
			offset = 0
			j = j + 1
			continue
		s0.getData(json_comment)
		offset = offset + 15
		time.sleep(1)

spider_maoyan()
