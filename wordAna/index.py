import jieba
import jieba.analyse as analyse
import os
import django
#引入django环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "douban_movies_analyst.settings")
django.setup()
from utils.getPublicData import getAllCommentsData

targetTxt = 'commentOne.txt'

def stopwordsList():
    stopwords = [line.strip() for line in open('./stopWords.txt',encoding='utf-8').readlines()]
    return stopwords

def seg_depart(sentence):
    sentence_depart = jieba.cut(" ".join(sentence).strip())
    stopwords = stopwordsList()
    outstr = ''
    for word in sentence_depart:
        if word not in stopwords:
            if word != '\t':
                outstr += word

    return outstr

def write_comment_One():
    with open(targetTxt, 'a+', encoding='utf-8') as targetFile:
        seg = jieba.cut(seg_depart(getAllCommentsData()),cut_all=False)
        output = ' '.join(seg)
        targetFile.write(output)
        targetFile.write('\n')
        print('写入成功！')

def main():
    write_comment_One()
    with open(targetTxt, 'r', encoding='utf-8') as file:
        text = file.readlines()
        keywords = jieba.analyse.extract_tags(str(text),topK=10,withWeight=True,allowPOS=())
        print(keywords)
        print('完成')

if __name__ == '__main__':
    main()










