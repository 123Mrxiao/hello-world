# -*- coding: utf-8 -*-
# 作者: 肖凯旋
# 日期：2020/2/3

import gevent
import time
import bs4
import requests
from gevent.queue import Queue
from gevent import monkey
monkey.patch_all()

proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"
# 代理隧道验证信息，根据购买的套餐，自行查看修改
proxyUser = "H37V4HC48S0K907D"
proxyPass = "524B0F78021A67ED"
proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass}

proxies = {
    "http": proxyMeta,
    "https": proxyMeta}

url_list = []

for i in range(1, 12):
    for x in range(1, 11):
        url_list.append("http://www.boohee.com/food/group/%d?page=%d" % (i, x))
    if i == 11:
        for x in range(1, 11):
            url_list.append("http://www.boohee.com/food/view_menu?page=%d" % x)

work = Queue()
for url in url_list:
    work.put_nowait(url)


def crawler():

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}

    while not work.empty():
        url = work.get_nowait()
        time.sleep(2)
        res = requests.get(url, headers=headers, proxies=proxies)
        bs_foods = bs4.BeautifulSoup(res.text, "html.parser")
        foods_list = bs_foods.find_all("li", class_="item clearfix")
        for food in foods_list:
            food_name = food.find_all("a")[1]["title"]
            food_url = "http://www.boohee.com" + food.find_all("a")[1]["href"]
            food_calorie = food.find('p').text
            print(food_name, food_url, food_calorie)


tasks_list = []
for x in range(3):
    task = gevent.spawn(crawler())
    tasks_list.append(task)
gevent.joinall(tasks_list)
