import json
import csv
import urllib
import time
import random
import requests
from lxml import etree
import re
from pymysql import *

# url https://movie.douban.com/subject/%7B%7D/reviews?start={}

conn = connect(host='localhost',user='root',password='xtj200441',db='douban_movies',port=3306,charset='utf8')

cursor = conn.cursor()

def querys(sql,params,type='no_select'):
    params = tuple(params)
    cursor.execute(sql,params)
    if type != 'no_select':
        data_list = cursor.fetchall()
        conn.commit()
        return data_list
    else:
        conn.commit()
        return 'sql执行成功！'

def getAllData():
    allData = querys('select * from movies',[],'select')
    with open('./top10MovieId.csv','a',newline='') as f:
        for i in range(10):
            f.write(allData[i][1] + '\n')
    return allData

def spider_main():
    with open('./top10MovieId.csv','r',newline='') as f:
        for i in  f.readlines():
            mId = re.findall(r'\d+',i)[0]
            for j in range(3):
                base_url = 'https://movie.douban.com/subject/{}/reviews?start={}'.format(mId,j * 20)
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
                    'Cookie': 'll="108309"; bid=SjJvyUP31Sk; __utma=30149280.1247025097.1737266150.1737266150.1737266150.1; __utmc=30149280; __utmz=30149280.1737266150.1.1.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmb=30149280.1.10.1737266150; ap_v=0,6.0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1737266154%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_id.100001.4cf6=65ba8423edcbb851.1737266154.; _pk_ses.100001.4cf6=1; __utma=223695111.493444712.1737266154.1737266154.1737266154.1; __utmb=223695111.0.10.1737266154; __utmc=223695111; __utmz=223695111.1737266154.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __yadk_uid=XZizupAH0rJsJzLQefpAY9DroTR1MLmG; _vwo_uuid_v2=DD321D9A29A36D7AE82099824D10284DE|b912fed729299262ae925ec15df4f4fe',
                }
                # 设置代理
                proxies = {
                    'http': 'http://8.220.204.215',  # 替换为你的 HTTP 代理
                    # 'https': 'http://127.0.0.1:57390',  # 替换为你的 HTTPS 代理
                }
                resp = requests.get(base_url, headers=headers, proxies=proxies)
                xpathHtml = etree.HTML(resp.text)
                try:
                    #电影名
                    movieName = xpathHtml.xpath('//*[@id="content"]/div/div[2]/div[1]/div[2]/a/text()')[0][2:]
                    #内容
                    divs = xpathHtml.xpath('//*[@id="content"]/div/div[1]/div[1]/div')

                    for div in divs:
                        content = div.xpath('.//div[@class="short-content"]/text()')
                        content = content[0].strip()
                        print(content)
                        if content != '':
                            querys('insert into comments(movieName,commentContent) values (%s, %s)',
                               [movieName, content])
                except Exception as e:
                    print(f"保存评论时出错: {e}")

                time.sleep(random.randint(1,10))



if __name__ == '__main__':
    # getAllData()
    spider_main()
















