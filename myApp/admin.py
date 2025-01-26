from django.contrib import admin
from myApp.models import *

class DbMovies(admin.ModelAdmin):
    list_display = ['id','detailLink','rate','title','cover',
                    'types','language','time','movieTime','comment_len',
                    'stars','summary','comments','imgList','movieUrl','createTime',
                    ]
    list_display_links = ['title']
    list_filter = ['country']
    search_fields = ['title']
    list_editable = ['detailLink']
    readonly_fields = ['id']
    list_per_page = 10
    date_hierarchy = 'createTime'
admin.site.register(Movies, DbMovies)

class usersA(admin.ModelAdmin):
    list_display = ['id','username','password','info',
                  ]
    list_display_links = ['username']
    search_fields = ['username']
    list_editable = ['info']
    readonly_fields = ['id']
    list_per_page = 10

admin.site.register(User, usersA)

class commentsA(admin.ModelAdmin):
    list_display = ['id','movieName','commentContent',
                  ]
    list_display_links = ['movieName']
    search_fields = ['movieName']
    list_editable = ['commentContent']
    readonly_fields = ['id']
    list_per_page = 10

admin.site.register(Comments, commentsA)

# Register your models here.
admin.site.site_header = '豆瓣电影信息管理'
admin.site.site_title = '豆瓣电影信息管理'

