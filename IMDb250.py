#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
from requests.exceptions import RequestException
import re
import io
import sys
import json
import pandas as pd

# 这个是为了解决windows下打印错误的问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


# 获取页面信息
def get_one_page(url):
	try:
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
		}
		response = requests.get(url, headers=headers)
		if response.status_code == 200:
			return response.text.replace('\n', '').replace('\t', '')
		return None
	except RequestException:
		return None


# 提取需要的信息并做成字典的形式a
def parse_one_page(html):
	pattern = re.compile(
		'chttp_tt_(.*?)\S>.*?href.*?/title/(.*?)/.*?title.*?>(.*?)</a>.*?>\((.*?)\)</span>.*?imdbRating.*?ratings\S\S(.*?)</strong>.*?"watchlistColumn">',
		re.S)
	items = re.findall(pattern, html)
	for item in items:
		yield {
			'排名': item[0],
			'IMDb链接': item[1],
			'名字': item[2],
			'上映日期': item[3],
			'分数': item[4]
		}


# 写入文件
def write_to_file(content):
	with open('imdb.txt', 'a', encoding='utf-8') as f:
		f.write(json.dumps(content, ensure_ascii=False) + '\n')


def write_xls(data):
	pf = pd.DataFrame(data)
	order = ['排名', 'IMDb链接', '名字', '上映日期', '分数']
	pf = pf[order]
	columns_map = {
		'排名': '排名',
		'IMDb链接':'IMDb链接',
		'名字': '名字',
		'上映日期': '上映日期',
		'分数': '评分'
	}
	pf.rename(columns=columns_map, inplace=True)
	file_path = pd.ExcelWriter('IMDb250.xlsx')
	pf.fillna(' ', inplace=True)
	pf.to_excel(file_path, encoding='utf-8', index=False)
	file_path.save()


def main():
	url = 'http://www.imdb.com/chart/top?ref_=nv_mv_250_6'
	html = get_one_page(url)
	result = []
	for item in parse_one_page(html):
		result.append(item)
	write_xls(result)
		# write_to_file(item)


main()
