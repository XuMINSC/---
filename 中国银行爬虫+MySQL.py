import time
import datetime
from datetime import timedelta#与时间/日期相关的包

import requests
import lxml.html
import numpy as np
import pandas as pd
import pymysql#用来向数据库写入文件

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'JSESSIONID=0000W3jyrnaX6V4ce5ggjwe0Fv4:-1',
    'Host': 'srh.bankofchina.com',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Mobile Safari/537.36'
}#爬虫请求头

#创建一个空表，规定列名
pounds = pd.DataFrame(columns = ['现汇买入价', '现钞买入价','现汇卖出价', '现钞卖出价', '中行折算价', '发布时间'])

#构造2262个网页链接，需要四个参数
#erectDate:2019-09-01;nothing=2020-09-14;page=1;pjname=英镑
timerange = []
for i in range(1,2262):
    timerange.append('https://srh.bankofchina.com/search/whpj/search_cn.jsp?erectDate=2019-09-01&nothing=2020-09-14&page={}&pjname=英镑'.format(i))


#创建一个函数，获取特定页码的汇率数据(不用翻页)
def get_rates(url):
    page = requests.get(url, headers = headers)
    lxmlobject = lxml.html.fromstring(page.text)

    info = lxmlobject.xpath('//div[@class="BOC_main publish"]')[0]
    info1 = info.xpath('string(.)')
    info2 = info1.split('英镑')

    global pounds
    for i in info2[1:len(info2)]:
        obs = i.replace('\t','').replace('\r','').split('\n')[1:7]
        newdf = pd.DataFrame(obs).T
        newdf.columns = pounds.columns
        pounds = pd.concat([pounds, newdf], axis = 0, ignore_index = True)
    return(pounds)

#爬取所有数据
for i in range(1000,2261):#共2262页
    get_rates(timerange[i])
    time.sleep(0.1)

#把数据去除重复
pounds.drop_duplicates(inplace = True)

##将数据写入MySQL数据库

#建立连接
conn=pymysql.connect(
    host='192.168.2.8',
    port=3306,
    user='root',
    password='Minxv145',
    db='minxu',#注意不是表名，而是数据库名
    charset='utf8')

#创建一个游标对象
cursor = conn.cursor(pymysql.cursors.DictCursor)

#使用execute()方法执行SQL查询
sql = ("insert into pounds (现汇买入价, 现钞买入价,现汇卖出价, 现钞卖出价, 中行折算价, 发布时间)" "values(%s,%s,%s,%s,%s,%s)")
for i in range(0,len(pounds)):#与行的数量有关，这个过程很快！
    sql = ("insert into pounds (现汇买入价, 现钞买入价,现汇卖出价, 现钞卖出价, 中行折算价, 发布时间)" "values(%s,%s,%s,%s,%s,%s)")
    data = (pounds.iloc[i,0],pounds.iloc[i,1],pounds.iloc[i,2],pounds.iloc[i,3],pounds.iloc[i,4],pounds.iloc[i,5])
    cursor.execute(sql,data)
    conn.commit()

#或者写入电脑内存
#pounds.to_csv("C:\\Users\\xumin\\Desktop\\pounds.csv")
