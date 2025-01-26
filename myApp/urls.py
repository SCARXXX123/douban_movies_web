from django.urls import path
from myApp import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("userInfo/",views.userInfo, name="userInfo"),
    path("changePassword/",views.changePassword, name="changePassword"),
    path("tableData/",views.tableData, name="tableData"),
    path("movie/",views.movie, name="movie"),
    path("search/",views.search, name="search"),
    path("typeChart/",views.typeChart, name="typeChart"),
    path("countryChart/",views.countryChart, name="countryChart"),
    path("commentChart/",views.commentChart, name="commentChart"),
    path("titleCloud/",views.titleCloud, name="titleCloud"),
    path("summaryCloud/",views.summaryCloud, name="summaryCloud"),
    path("timeChart/",views.timeChart, name="timeChart"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
]