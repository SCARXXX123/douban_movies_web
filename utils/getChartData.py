import csv
import json
from snownlp import SnowNLP
from myApp.models import *
from utils.getPublicData import *
from datetime import datetime
import ast
import re

from utils.error import *


allData = getAllData()

def getMaxRate():
    rateList =[x.rate for x in allData]
    titleList = [x.title for x in allData]
    print(rateList)
    maxRate = max(map(float,rateList))
    maxTitle = titleList[rateList.index(str(maxRate))]#maxRate的索引也对应着maxTile的索引
    # print(maxRate)
    # print(maxTitle)
    return maxRate,maxTitle

def getMaxCommentLen():
    CommentLenList = [x.comment_len for x in allData]
    maxComLen = max(map(int,CommentLenList))
    print(maxComLen)
    return maxComLen

def getMaxMovieTime():
    MovieTimeList = [x.movieTime for x in allData]
    MaxmvTime = max(map(int, MovieTimeList))
    print(MaxmvTime)
    return MaxmvTime


def getMinTime():
    timeList = [x.time for x in allData]
    now = datetime.now()

    # 安全地处理可能是字符串列表的情况
    date_objects = []
    for date in timeList:
        # 如果是字符串列表，提取第一个元素
        if isinstance(date, str) and date.startswith('[') and date.endswith(']'):
            date = ast.literal_eval(date)[0]

            # 解析日期
        date_objects.append(datetime.strptime(date, '%Y-%m-%d'))

    minTime = min(date_objects, key=lambda x: abs(x - now))
    minTime = minTime.strftime('%Y-%m-%d')
    print(minTime)
    return minTime

def getTypesAll():
    types = {}
    for i in allData:
        for j in i.types:
            if types.get(j,-1) == -1:
                types[j] = 1
            else:
                types[j] += 1
    # print(types)
    maxTypeLen = len(list(types.values()))
    maxType = max(types.keys(), key=lambda x: types[x])
    # print(maxType)
    # print(maxTypeLen)
    return maxTypeLen,maxType

def getAllRateData():
    dataDic ={}
    for i in allData:
        if dataDic.get(float(i.rate),-1) == -1:
            dataDic[float(i.rate)] = 1
        else:
            dataDic[float(i.rate)] += 1
    dataDic = sorted(dataDic.items(), key=lambda x: x[0], reverse=True)
    xData = []
    yData = []
    for i in dataDic:
        xData.append(i[0])
        yData.append(i[1])
    return xData[:10],yData[:10]

def getAllUser():
    allUser = list(User.objects.all())
    userDic = {}
    for i in allUser:
        if userDic.get(i.username,-1) == -1:
            userDic[i.username] = 1
    userPieData =[]
    for k,v in userDic.items():
        userPieData.append({
            'name':k,
            'value':v
        })
    print(userPieData)
    return userPieData

def getAllMovies():
    moviesList = []
    for i in allData:
        moviesList.append(i.title)
    print(moviesList)
    return moviesList

def getMovieInfoDetail(movieName):
    movieInfo = []
    for i in allData:
        if i.title == movieName:
            movieInfo = i
    # print(movieInfo.title)
    return movieInfo

def changeSelfInfo(newInfo,fileInfo,uname):
    user = User.objects.get(username=uname)
    user.info = newInfo.get('info')
    if fileInfo.get('avatar') != None:
        user.avatar = fileInfo.get('avatar')
    user.save()

def changePasswordTwo(uname,passwordInfo):
    oldPwd = passwordInfo.get('oldPassword')
    newPwd = passwordInfo.get('newPassword')
    checkPasswod = passwordInfo.get('checkPassword')

    user = User.objects.get(username=uname)

    if oldPwd != user.password:return '原密码不正确'
    if newPwd != checkPasswod: return '两次密码输入不一致'

    user.password = newPwd
    user.save()

def getMovieById(id):
    movieInfo = []
    for i in allData:
        if int(i.id) == int(id):
            movieInfo = i
    print(movieInfo.title)
    return movieInfo

def getPostData(word):
    movieInfos = Movies.objects.filter(title__contains=word)

    def map_fn(item):
        item.rate = float(item.rate) * 10
        # 类型
        if isinstance(item.types, str):
            item.types = item.types.split(',')

            # 国家
        if item.country is None:
            item.country = '中国'
        elif isinstance(item.country, str):
            item.country = item.country.split(',')

            # 语言
        if item.language is None:
            item.language = '普通话'
        elif isinstance(item.language, str):
            item.language = item.language.split('.')

            # 评分
        if isinstance(item.stars, str):
            item.stars = item.stars.split('%.')
            item.stars = [x + "%" for x in item.stars]

            # 图片链接
        if isinstance(item.imgList, str):
            item.imgList = item.imgList.split('g.')
            item.imgList = [x + 'g' for x in item.imgList]

            # 评论
        if isinstance(item.comments, str):
            item.comments = json.loads(item.comments)

        return item

    movieInfos = list(map(map_fn, list(movieInfos)))  # 注意这里改为 movieInfos

    if movieInfos:
        print(movieInfos)
    else:
        print('没有找到此电影')

    return movieInfos

def getTypePieChartData():
    typeData = {}
    for i in allData:
        for j in i.types:
            if typeData.get(j,-1) == -1:
                typeData[j] = 1
            else:
                typeData[j] += 1
    typePieData = []
    for k,v in typeData.items():
        typePieData.append({
            'name':k,
            'value':v
        })
    # print(typePieData)
    return typePieData[:9]

def getTypeBarChartData():
    #取出数量与类型的键值对
    typeData = {}
    for i in allData:
        for j in i.types:
            if typeData.get(j,-1) == -1:
                typeData[j] = 1
            else:
                typeData[j] += 1

    #将类型放进rateData
    rateData = {}
    for k,v in typeData.items():
        if rateData.get(k,-1) == -1:
            rateData[k] = []

    #是相同类型就把评分加入rateData
    for i in allData:
        for key,value in rateData.items():
            for j in i.types:
                if j == key:
                    value.append(float(i.rate))

    # 计算平均分
    for key,value in rateData.items():
        sum = 0
        for item in value:
            sum += item
        rateData[key] = round(sum / len(value),1)
    # print(rateData)
    return list(typeData.keys()),list(typeData.values()),list(rateData.values())

def getCountryChartData():
    countryDic = {}
    for i in allData:
        for j in i.country:
            if countryDic.get(j,-1) == -1:
                countryDic[j] = 1
            else:
                countryDic[j] += 1
    # print(countryDic)
    countrySortData = sorted(countryDic.items(), key=lambda x: x[1], reverse=True)
    # print(countrySortData)
    countryX = []
    countryY = []
    for i in countrySortData:
        countryX.append(i[0])
        countryY.append(i[1])
    # print(countryX,countryY)
    return countryX[:10],countryY[:10]

def getLanguageChartData():
    languageData = {}
    for i in allData:
        for j in i.language:
            if languageData.get(j,-1) == -1:
                languageData[j] = 1
            else:
                languageData[j] += 1
    # print(languageData)
    languageDataEnd = []
    for k,v in languageData.items():
        languageDataEnd.append({
            'name':k,
            'value':v
        })
    # print(languageDataEnd)
    return languageDataEnd[:10]


def getPubTimeData():
    monthData = {}
    try:
        for i in allData:
            # 处理列表形式的时间
            if isinstance(i.time, list):
                # 遍历列表中的时间
                for time_str in i.time:
                    # 使用正则表达式匹配标准日期格式
                    match = re.search(r'\d{4}-\d{2}-\d{2}', str(time_str))
                    if match:
                        time_str = match.group()

                        data_obj = datetime.strptime(time_str, '%Y-%m-%d')
                        month = data_obj.strftime('%m')

                        monthData[month] = monthData.get(month, 0) + 1
            else:
                # 处理非列表情况
                time_str = str(i.time)
                match = re.search(r'\d{4}-\d{2}-\d{2}', time_str)
                if match:
                    time_str = match.group()

                    data_obj = datetime.strptime(time_str, '%Y-%m-%d')
                    month = data_obj.strftime('%m')

                    monthData[month] = monthData.get(month, 0) + 1
    except Exception as e:
        print(f"Error processing time data: {e}")
        print(f"Problematic time data: {i.time}")
    # print(monthData)

    sorted_d = dict(sorted(monthData.items()))
    # print(sorted_d)

    rateData= {}
    for i in sorted_d:
        if rateData.get(i,-1) == -1:
            rateData[i] = []

    for i in allData:
        for k,v in rateData.items():
            if isinstance(i.time, list):
                # 遍历列表中的时间
                for time_str in i.time:
                    # 使用正则表达式匹配标准日期格式
                    match = re.search(r'\d{4}-\d{2}-\d{2}', str(time_str))
                    if match:
                        time_str = match.group()

                        data_obj = datetime.strptime(time_str, '%Y-%m-%d')
                        month = data_obj.strftime('%m')

                        monthData[month] = monthData.get(month, 0) + 1
                        if month == k:
                            v.append(float(i.rate))
            else:
                # 处理非列表情况
                time_str = str(i.time)
                match = re.search(r'\d{4}-\d{2}-\d{2}', time_str)
                if match:
                    time_str = match.group()

                    data_obj = datetime.strptime(time_str, '%Y-%m-%d')
                    month = data_obj.strftime('%m')
                    if month == k:
                        v.append(float(i.rate))


    for k,v in rateData.items():
        sum = 0
        for item in v:
            sum += item
        rateData[k] = round(sum / len(v),1)

    # print(rateData)

    timeX = list(rateData.keys())#月份
    timeY1 = list(monthData.values())#个数
    timeY2 = list(rateData.values())#平均分
    timeXNew = []
    for i in timeX:
        timeXNew.append(i + '月')
    # print(timeXNew)

    return timeXNew, timeY1, timeY2

def getTimeLen():
    timeData = [{
        'name': '很长',
        'value': 0
    },
    {
        'name': '长',
        'value': 0
    },
    {
        'name': '中',
        'value': 0
    },
    {
        'name': '短',
        'value': 0
    },
    {
        'name': '很短',
        'value': 0
    },
    ]
    for i in allData:
        if int(i.movieTime) < 50:
            timeData[4]['value'] += 1
        elif int(i.movieTime) < 80:
            timeData[3]['value'] += 1
        elif int(i.movieTime) < 120:
            timeData[2]['value'] += 1
        elif int(i.movieTime) < 150:
            timeData[1]['value'] += 1
        else:
            timeData[0]['value'] += 1
    # print(timeData)
    return timeData

def getAllHostData():
    xData = []
    yData = []

    try:
        with open('./wordAna/commentTwo.csv', 'r', encoding='utf-8') as renders:
            reader = csv.reader(renders)
            for i in reader:
                xData.append(re.search('[\u4e00-\u9fa5]+', i[0]).group())#只提取汉字
                yData.append(int(re.search('\d+', i[1]).group()))#只提取数字
    except Exception as e:
        print(f"Error processing all host data: {e}")
        pass
    # print(xData, yData)
    return xData[:15], yData[:15]

def getAllHostDetail():
    xData = ['0.1','0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9','1.0']
    yData = [0,0,0,0,0,0,0,0,0,0]
    commentList = getAllCommentsData()[:300]
    result = [
        {
            'name': '积极',
            'value': 0,
        },
        {
            'name': '消极',
            'value': 0,
        },
    ]
    for i in commentList:

        try:
            value = SnowNLP(i).sentiments
            if value >= 0.5:
                result[0]['value'] += 1
            elif value >= 0:
                result[1]['value'] += 1

            if value >= 0.9:
                yData[9] += 1
            elif value >= 0.8:
                yData[8] += 1
            elif value >= 0.7:
                yData[7] += 1
            elif value >= 0.6:
                yData[6] += 1
            elif value >= 0.5:
                yData[5] += 1
            elif value >= 0.4:
                yData[4] += 1
            elif value >= 0.3:
                yData[3] += 1
            elif value >= 0.2:
                yData[2] += 1
            elif value >= 0.1:
                yData[1] += 1
            elif value == 0:
                yData[0] += 1

        except Exception as e:
            print(f"Error processing all host data: {e}")
            continue
    # print(yData)
    print(result)
    return xData, yData,result
