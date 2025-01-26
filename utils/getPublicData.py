import json
from myApp.models import *
import sys
import traceback
def getAllData():
    def map_fn(item):
        #类型
        item.types = item.types.split(',')

        #国家
        if item.country == None:
            item.country = '中国'
        else:
            item.country = item.country.split(',')

        #语言
        if item.language == None:
            item.language = '普通话'
        else:
            item.language = item.language.split('.')

        #评分
        item.stars = item.stars.split('%.')
        def add_a(list):
            return [x + "%" for x in list]
        item.stars = add_a(item.stars)

        #图片链接
        item.imgList = item.imgList.split('g.')
        def add_p(list):
            return [x + 'g' for x in list]
        item.imgList = add_p(item.imgList)

        #评论
        item.comments = json.loads(item.comments)

        return item

    allData = Movies.objects.all()
    allData = list(map(map_fn,list(allData)))

    try:
        print(allData)
    except(TypeError, NameError):
        # 打印完整的错误追踪信息
        print("Full Error Traceback:")
        traceback.print_exc()

    return allData

def getAllCommentsData():#获取电影的前5条评论
    allData = Movies.objects.all()
    commentList = []
    for i in allData:
        comments = json.loads(i.comments)
        for c in comments:
            commentList.append(c['comments'])
    # print(commentList[0])
    return commentList

# def getAllCommentsDataTwo():#获取电影的全部评论,from commentTable
#     commentsData = Comments.objects.all()
#     commentList = []
#     for i in commentsData:
#         commentList.append(i.commentContent)
#     print(commentList[5])