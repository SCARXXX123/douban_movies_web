import jieba
import jieba.analyse as analyse
import re
import os
import django
#引入django环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "douban_movies_analyst.settings")
django.setup()
from utils.getPublicData import getAllCommentsData

#打开文件
reader = open('./commentOne.txt', 'r', encoding='utf-8')
strs = reader.read()
result = open('commentTwo.csv', 'w', encoding='utf-8')

#分词
word_list = jieba.cut(strs,cut_all=True)

new_word = []
for i in word_list:
    m = re.search("\d+",i)#去掉数字
    n = re.search('\W+',i)#去掉非字符
    if not m and not n and len(i) > 1:#不要数字和非单词
        new_word.append(i)

word_count = {}
for i in set(new_word):
    word_count[i] = new_word.count(i)
print(word_count)

list_count = sorted(word_count.items(), key=lambda co:co[1], reverse=True)#出现频次作为排序依据

for i in range(300):
    print(list_count[i],file=result)
