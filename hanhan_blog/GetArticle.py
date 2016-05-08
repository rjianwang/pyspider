#! /usr/bin/env python
# coding:utf-8

import urllib
import re
import csv

str0 = 'http://blog.sina.com.cn/s/blog_4701280b0102dz9f.html'
str1 = 'http://blog.sina.com.cn/s/articlelist_1191258123_0_1.html'

#     describe: 获取文章		
# article_list: 文章网址列表
def GetArticle(article_list):
	for item in article_list:
#		SaveAsHtml(item, r'article/')
		SaveAsTxt(item, r'txt/')

#  describe: 获取文章地址列表
# page_list: 存储文章列表网址的列表
#    return: 返回文章网址列表
def GetArticleList(page_list):
	article_list = [] 
	for item in page_list:
		content   = urllib.urlopen(item).read()

		title = content.find(r'<a title=')
		href  = content.find(r'href=', title)
		html  = content.find(r'.html', href)
		url   = content[href + 6: html + 5]

		while title != -1 and href != -1 and html != -1:
			article_list.append(url)
			title = content.find(r'<a title=', html)
			href  = content.find(r'href=', title)
			html  = content.find(r'.html', href)
			url   = content[href + 6: html + 5]

	return article_list

# describe: 获取文章列表分页网址
#      url: 文章列表第一页的网址
#   return: 返回文章分页网址列表
def GetArticlePages(url):
	page_list = []
	page_list.append(url)

	content = urllib.urlopen(url).read()
	pgon = content.find(r'<li class="SG_pgon"')
	pgnext = content.find(r'<li class="SG_pgnext"')

	href = content.find(r'<a href=', pgon)
	html = content.find(r'.html', href)
	url  = content[href + 9: html + 5]

	while href != -1 and html != -1:
		page_list.append(url)
		href = content.find(r'<a href=', html, pgnext)
		html = content.find(r'.html', href, pgnext)
		url = content[href + 9: html + 5]

	return page_list

def SaveAsHtml(url, path):
	content = urllib.urlopen(url).read()
	filename = url[-26: ]
	open(path + filename, 'w+').write(content)


def SaveAsTxt(url, path):
	content = urllib.urlopen(url).read()

	title = content.find(r'titName SG_txta')
	temp  = content.find(r'</h2>', title)
	article_name = content[title + 17: temp]
	article_name = re.sub(r'&nbsp;', ' ', article_name)
	article_name = re.sub(r'&[lg]t;', '', article_name)
	
	date  = content.find(r'time SG_txtc', temp)
	temp  = content.find(r'</span>', date)
	article_date = content[date + 15: temp - 1]

	# save articles's name and date in a csv file   
	csvfile = file('hanhan.csv', 'a+')
	writer = csv.writer(csvfile)
	writer.writerow([article_name, article_date])
	
	begin = content.find(r'<!-- 正文开始 -->')
	end   = content.find(r'<!-- 正文结束 -->', begin)
	content = content[begin + 21:end]
	
	regex = re.compile(r'</?\w+[^>]*>')
	#regex = re.compile(r'<[^>]+>')
	content = re.sub(regex, '', content)
	content = re.sub(r'&nbsp;', '', content)

	filename = article_name + '(' + article_date + ').txt'
	open(path + filename, 'w+').write(content)
	
page_list = GetArticlePages(str1)
article_list = GetArticleList(page_list)

#a = []
#a.append(str0)
#GetArticle(a)

GetArticle(article_list)
