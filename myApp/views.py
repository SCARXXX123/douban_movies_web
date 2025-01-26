from django.shortcuts import render,redirect
from myApp.models import User,Comments,Movies
from utils.error import *
from utils.getPublicData import *
from utils.getChartData import *
# Create your views here.
def home(request):
    try:
        uname = request.session.get('username')
        userInfo = User.objects.get(username=uname)
        # getAllData()
        maxRate,maxTitle = getMaxRate()
        maxComLen = getMaxCommentLen()
        MaxmvTime = getMaxMovieTime()
        minTime = getMinTime()
        maxTypeLen,maxType = getTypesAll()
        xData,yData = getAllRateData()
        userPieData = getAllUser()
        moviesList = getAllMovies()
        defaultMovie = request.GET.get('movieName') or '隐藏的面孔'
        movieInfo = getMovieInfoDetail(defaultMovie)
    except Exception as e:
        print(e)
        return redirect('login')

    return render(request,'index.html',{
        'userInfo':userInfo,
        'maxRate': maxRate,
        'maxTitle': maxTitle,
        'maxComLen': maxComLen,
        'MaxmvTime': MaxmvTime,
        'minTime': minTime,
        'maxTypeLen': maxTypeLen,
        'maxType': maxType,
        'xData': xData,
        'yData': yData,
        'userPieData': userPieData,
        'moviesList': moviesList,
        'movieInfo': movieInfo,
    })

def userInfo(request):
    try:
        uname = request.session.get('username')
        userInfo = User.objects.get(username=uname)
        # getAllData()
        print(request.POST,request.FILES)
        if request.method == 'POST':
            changeSelfInfo(request.POST,request.FILES,uname)
            userInfo = User.objects.get(username=uname)
    except Exception as e:
        print(e)
        return redirect('login')

    return render(request, 'userInfo.html', {
        'userInfo':userInfo,
    })

def changePassword(request):
    try:
        uname = request.session.get('username')
        userInfo = User.objects.get(username=uname)
        # getAllData()
        if request.method == 'POST':
            print(request.POST)
            res = changePasswordTwo(uname,request.POST)
            if res != None:
                return errorRespose(request,res)
            userInfo = User.objects.get(username=uname)
    except Exception as e:
        print(e)
        return redirect('login')

    return render(request, 'changePassword.html', {
        'userInfo':userInfo,
    })

def tableData(request):
    try:
        uname = request.session.get('username')
        userInfo = User.objects.get(username=uname)
        # getAllData()
        tableData = getAllData()
    except Exception as e:
        print(e)
        return redirect('login')

    return render(request, 'tableData.html', {
        'userInfo':userInfo,
        'tableData':tableData,
    })

def movie(request):
    try:
        uname = request.session.get('username')
        userInfo = User.objects.get(username=uname)
        movieInfo = getMovieById(request.GET.get('id'))
    except Exception as e:
        print(e)
        return redirect('login')

    return render(request, 'movie.html', {
        'userInfo':userInfo,
        'movieInfo':movieInfo
    })

def search(request):
    try:
        uname = request.session.get('username')
        userInfo = User.objects.get(username=uname)
        if request.method == 'POST':
            print(request.POST.get('searchWord'))
            movieInfos = getPostData(request.POST.get('searchWord'))
            return render(request, 'search.html', {
                'userInfo': userInfo,
                'movieInfos': movieInfos,
            })
    except Exception as e:
        print(e)
        return redirect('login')

    return render(request, 'search.html', {
        'userInfo':userInfo,
    })

def typeChart(request):
    try:
        uname = request.session.get('username')
        userInfo = User.objects.get(username=uname)
        # getAllData()
        typePieData = getTypePieChartData()
        XData,yData1,yData2=getTypeBarChartData()
    except Exception as e:
        print(e)
        return redirect('login')

    return render(request, 'typeChart.html', {
        'userInfo':userInfo,
        'typePieData':typePieData,
        'XData':XData,
        'yData1':yData1,
        'yData2':yData2,
    })

def countryChart(request):
    try:
        uname = request.session.get('username')
        userInfo = User.objects.get(username=uname)
        # getAllData()
        countryX,countryY = getCountryChartData()
        languageDataEnd = getLanguageChartData()
    except Exception as e:
        print(e)
        return redirect('login')

    return render(request, 'countryChart.html', {
        'userInfo':userInfo,
        'countryX':countryX,
        'countryY':countryY,
        'languageDataEnd':languageDataEnd,
    })

def timeChart(request):
    try:
        uname = request.session.get('username')
        userInfo = User.objects.get(username=uname)
        timeXNew, timeY1, timeY2 = getPubTimeData()
        timeData = getTimeLen()

    except Exception as e:
        print(e)
        return redirect('login')

    return render(request, 'timeChart.html', {
        'userInfo':userInfo,
        'timeXNew':timeXNew,
        'timeY1':timeY1,
        'timeY2':timeY2,
        'timeData':timeData,
    })

def commentChart(request):
    try:
        uname = request.session.get('username')
        userInfo = User.objects.get(username=uname)
        xData1,yData1 = getAllHostData()#词频
        xData2,yData2,result = getAllHostDetail()#情感分析
    except Exception as e:
        print(e)
        return redirect('login')

    return render(request, 'commentChart.html', {
        'userInfo':userInfo,
        'xData1':xData1,
        'yData1':yData1,
        'xData2':xData2,
        'yData2':yData2,
        'result':result,
    })

def titleCloud(request):
    try:
        uname = request.session.get('username')
        userInfo = User.objects.get(username=uname)

    except Exception as e:
        print(e)
        return redirect('login')

    return render(request, 'titleCloud.html', {
        'userInfo':userInfo,
    })

def summaryCloud(request):
    try:
        uname = request.session.get('username')
        userInfo = User.objects.get(username=uname)

    except Exception as e:
        print(e)
        return redirect('login')

    return render(request, 'summaryCloud.html', {
        'userInfo':userInfo,
    })

def login(request):
    if request.method == "GET":
        return render(request, 'page-login.html', {})
    else:
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        try:
            user = User.objects.get(username=uname,password=pwd)#获取数据库数据
            print(uname,pwd)
            request.session['username'] = user.username
            return redirect('home')
        except:
            return errorRespose(request,'请输入正确的用户名和密码/Please enter the correct username and password')

def logout(request):
    request.session.clear()
    return redirect('login')



def register(request):
    if request.method == "GET":
        return render(request,'page-register.html',{})
    else:
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        checkPwd = request.POST.get('checkPassword')
        print(uname,pwd,checkPwd)
        try:
            User.objects.get(username=uname)
        except:
            if not uname or not pwd or not checkPwd: return errorRespose(request,'不允许为空！/Cannot be empty')
            if pwd != checkPwd: return errorRespose(request,'两次密码不一致！/Passwords do not match')
            User.objects.create(username=uname,password=pwd)
            return redirect('/myApp/login')
        return errorRespose(request,'该邮箱已被注册！/This email address has been registered')

