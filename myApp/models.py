from django.db import models

# Create your models here.

class Movies(models.Model):
    id = models.AutoField('id', primary_key=True)#自动添加，主键
    detailLink = models.TextField('图片列表', blank=True, null=True)
    rate = models.CharField('评分', max_length=255,default='')
    title = models.CharField('电影名',max_length=255,default='')
    cover = models.CharField('封面', max_length=255,default='')
    year = models.CharField('年份', max_length=255,default='')
    types = models.CharField('类型', max_length=255,default='')
    country = models.CharField('国家', max_length=255,default='')
    language = models.CharField('语言', max_length=255,default='')
    time = models.CharField('时间', max_length=255,default='')
    movieTime = models.CharField('电影时长', max_length=255,default='')
    comment_len = models.CharField('评论量', max_length=255,default='')
    stars = models.CharField('星级', max_length=255,default='')
    summary = models.TextField('图片列表', blank=True, null=True)
    comments = models.TextField('图片列表', blank=True, null=True)
    imgList = models.TextField('图片列表', blank=True, null=True)
    movieUrl = models.TextField('视频链接', blank=True, null=True)
    createTime = models.DateField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'movies'

class Comments(models.Model):
    id = models.AutoField('id', primary_key=True)
    movieName = models.CharField('电影名',max_length=255,default='')
    commentContent = models.TextField('电影评论', blank=True, null=True)

    class Meta:
        db_table = 'comments'

class User(models.Model):
    id = models.AutoField('id', primary_key=True)
    username = models.CharField('用户名',max_length=255,default='')
    password = models.CharField('密码',max_length=255,default='')
    info = models.CharField('个人描述',max_length=255,default='')
    avatar = models.FileField('用户头像',upload_to='avatar',default='avatar/default.png')

    class Meta:
        db_table = 'user'



