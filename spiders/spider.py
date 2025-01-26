import csv
import os
import django
import requests
import re
import jsonpath
import pandas as pd
import random
import time
from bs4 import BeautifulSoup
import json
import datetime
import requests
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "douban_movies_analyst.settings")
django.setup()
from myApp.models import Movies

# url https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0
# url https://movie.douban.com/subject/%7B%7D/reviews?start={}
def spider(spiderTarget,start):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
        'Cookie':'ll="108309"; bid=SjJvyUP31Sk; __utma=30149280.1247025097.1737266150.1737266150.1737266150.1; __utmc=30149280; __utmz=30149280.1737266150.1.1.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmb=30149280.1.10.1737266150; ap_v=0,6.0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1737266154%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_id.100001.4cf6=65ba8423edcbb851.1737266154.; _pk_ses.100001.4cf6=1; __utma=223695111.493444712.1737266154.1737266154.1737266154.1; __utmb=223695111.0.10.1737266154; __utmc=223695111; __utmz=223695111.1737266154.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __yadk_uid=XZizupAH0rJsJzLQefpAY9DroTR1MLmG; _vwo_uuid_v2=DD321D9A29A36D7AE82099824D10284DE|b912fed729299262ae925ec15df4f4fe',
    }

    params = {
        'page_start':start,
    }

    # # 设置代理
    proxies = {
        'http': 'http://8.220.204.215',  # 替换为你的 HTTP 代理
        # 'https': 'http://127.0.0.1:57390',  # 替换为你的 HTTPS 代理
    }

    movieAllRes = requests.get(spiderTarget,headers=headers,params=params,proxies=proxies)
    movieAllRes = movieAllRes.json()

    moviesInformation = jsonpath.jsonpath(movieAllRes,'$.subjects')[0]
    print(moviesInformation)

    detailUrls = jsonpath.jsonpath(movieAllRes,'$.subjects..url')
    for i,movieInformation in enumerate(moviesInformation):
        resultData = {}
        resultData['detailLink'] = detailUrls[i]
        #rate
        resultData['rate'] = movieInformation['rate']
        #title
        resultData['title'] = movieInformation['title']
        #cover
        resultData['cover'] = movieInformation['cover']

        #-------详情页------
        print(resultData)
        detaiUrlsRes = requests.get(detailUrls[i],headers=headers)
        soup = BeautifulSoup(detaiUrlsRes.text,'lxml')

        #上映年份
        #正则表达，去除年份的括号
        try:
            resultData['year'] = re.findall('[(](.*?)[)]',soup.find('span',class_='year').get_text())[0]
        except (AttributeError, IndexError):
            continue
            # print(resultData)

        #影片类型
        types = soup.find_all('span',property='v:genre')
        for i,span in enumerate(types):#不止有一个标签
            types[i] = span.get_text()
        resultData['types'] = ','.join(types)
        # print(resultData)

        #制片国家
        country = soup.find_all('span',class_='pl')[4].next_sibling.strip().split(sep='/')
        for i,span in enumerate(country):#不止有一个国家
            country[i] = span.strip()
        resultData['country'] = ','.join(country)
        # print(resultData)

        #影视语言
        language = soup.find_all('span', class_='pl')[5].next_sibling.strip().split(sep='/')
        for i, span in enumerate(language):  # 不止有一种语言
            language[i] = span.strip()
        resultData['language'] = ','.join(language)
        # print(resultData)

        #上映时间
        upTimes = soup.find_all('span',property='v:initialReleaseDate')
        upTimesStr = ''
        for i in upTimes:
            upTimesStr = upTimesStr + i.get_text() + ','
        upTime = re.findall(r'(\d*-\d*-\d*)',upTimesStr)
        resultData['Time'] = upTime
        # print(resultData)

        #时长
        if soup.find_all('span',property='v:runtime'):
            # resultData['movietime'] = soup.find('span', property='v:runtime').get_text()
            resultData['movietime'] = re.findall('\d+',soup.find('span',property='v:runtime').get_text())[0]
        else:
            resultData['movietime'] = 0
        # print(resultData)

        #评论个数
        resultData['comment_num'] = soup.find('span',property='v:votes').get_text()

        #星星比例
        stars = []
        starAll = soup.find_all('span',class_='rating_per')
        for i in starAll:
            stars.append(i.get_text())
        resultData['stars'] = '.'.join(stars)
        # print(resultData)

        #影片简介
        resultData['summary'] = soup.find('span',property='v:summary').get_text().strip()
        # print(resultData)

        #5条热评
        #发布者信息
        comment_info = soup.find_all('span',class_='comment-info')
        comments = [{} for x in range(5)]
        for i,comment in enumerate(comment_info):
            comments[i]['user'] = comment.contents[1].get_text()
            comments[i]['star'] = re.findall(r'(\d*)',comment.contents[5].attrs['class'][0])[7]
            try:
                comments[i]['time'] = comment.contents[7].attrs['title']
            except:
                comments[i]['time'] = '2024-09-01 12:03:23'
        #评论信息
        contents = soup.find_all('span',class_='short')
        for i in range(5):
            comments[i]['comments'] = contents[i].get_text()
        resultData['comments'] = json.dumps(comments)
        # print(resultData['comments'])

        #图片
        imgList = []
        lis = soup.select('.related-pic-bd img')
        for i in lis:
            imgList.append(i['src'])
        resultData['imgList'] = '.'.join(imgList)
        # print(resultData['imgList'])

        #视频
        if soup.find('a',class_='related-pic-video'):
            movieUrl = soup.find('a',class_='related-pic-video').attrs['href']
            foreshowMovieRes = requests.get(movieUrl,headers=headers)
            foreshowMovieRes = BeautifulSoup(foreshowMovieRes.text,'lxml')
            movieUrl = foreshowMovieRes.find('source').attrs['src']
            resultData['movieUrl'] = movieUrl
        else:
            resultData['movieUrl'] = '0'
        print(resultData)

        result.append(resultData)
        resultDateValue = list(resultData.values())
        save_to_scvTwo(resultDateValue)
        print('已经爬取%d条数据'%len(result))

        # break

def save_to_csv(df):
    df.to_csv('./datas.csv')

def save_to_scvTwo(rowData):
    with open('./datasTwo.csv','a',newline='',encoding='utf-8') as wf:
        writer = csv.writer(wf)
        writer.writerow(rowData)

def main():#控制翻页
    global result #接受每一次循环的结果
    result = []
    with open('./pagenNum.txt','r') as fr:
        page = int(fr.readlines()[-1])
        print('开始爬取第%s个20' % page)
        spider(spiderTarget,page * 20)

        time.sleep(random.randint(1,10))
        df = pd.DataFrame(result)
        # save_to_csv(df)
        # print('储存为csv文件成功！')
        with open('./pagenNum.txt','a') as fa:
            fa.write('\n' + str(page + 1)  )

        result = []
        for i in range(len(result)):
            result.pop()

    main()

def clear_csv():
    df = pd.read_csv('./datasTwo.csv')
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    return df.values

def save_to_sql():
    data = clear_csv()
    print('正在保存数据')
    for movie in data:
        try:
            Movies.objects.create(
                detailLink=movie[0],
                rate=movie[1],
                title=movie[2],
                cover=movie[3],
                year=movie[4],
                types=movie[5],
                country=movie[6],
                language=movie[7],
                time=movie[8],
                movieTime=movie[9],
                comment_len=movie[10],
                stars=movie[11],
                summary=movie[12],
                comments=movie[13],
                imgList=movie[14],
                movieUrl=movie[15],
            )
        except Exception as e:
            print(f"保存数据时出错: {e}")
    print('保存成功')



if __name__ == '__main__':
    print('爬取开始！')
    spiderTarget = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20'
    # spider(spiderTarget,0)
    # main()
    save_to_sql()



