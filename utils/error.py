from django.shortcuts import render

def errorRespose(request,errMsg):
    return render(request,'page-404.html',
                  {
                      'errMsg':errMsg,
                  })