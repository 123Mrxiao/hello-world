# -*- coding: utf-8 -*-
# 作者: 肖凯旋
# 日期：2020/2/4

import scrapy
from bs4 import BeautifulSoup
from ..items import DoubanItem


class DoubanSpiders(scrapy.Spider):
    # 定义名字，是爬虫的唯一标识
    name = "douban"
    # 添加域名，让爬虫在当前域名范围内爬取
    allowed_domains = ["book.douban.com"]
    # 定义爬取的网页网址列表
    start_urls = []
    # 爬取三页
    for i in range(3):
        # 拼接URL
        url = "https://book.douban.com/top250?start=" + str(i * 25)
        # 添加进列表
        start_urls.append(url)

    def parse(self, response):
        bs = BeautifulSoup(response.text, "html.parser")
        datas = bs.find_all("tr", class_="item")

        for data in datas:
            item = DoubanItem()
            # 实例化DoubanItem这个类。
            item['title'] = data.find_all('a')[1]['title']
            # 提取出书名，并把这个数据放回DoubanItem类的title属性里。
            item['publish'] = data.find('p', class_='pl').text
            # 提取出出版信息，并把这个数据放回DoubanItem类的publish里。
            item['score'] = data.find('span', class_='rating_nums').text
            # 提取出评分，并把这个数据放回DoubanItem类的score属性里。
            print(item['title'])
            # 打印书名。
            yield item
            # yield item是把获得的item传递给引擎。

