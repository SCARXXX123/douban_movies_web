import jieba
from matplotlib import pyplot as plt
from wordcloud import WordCloud
import numpy as np
from PIL import Image
from pymysql import *

def get_img(field,targetImageSrc,resImageSrc):
    conn = connect(host='localhost', port=3306, user='root', passwd='xtj200441', db='douban_movies',charset='utf8mb4')
    cursor = conn.cursor()
    sql = f"select {field} from movies"
    cursor.execute(sql)
    data = cursor.fetchall()

    text = ""
    for i in data:
        if i[0] != '':
            tarArr = i
            for j in tarArr:
                text += j

    cursor.close()
    conn.close()

    data_cut = jieba.cut(text,cut_all=True)

    string = ' '.join(data_cut)

    #生成词云图
    img = Image.open(targetImageSrc)
    img_arr = np.array(img)
    wc = WordCloud(
        background_color='#292929',
        font_path='STHUPO.TTF',
        mask = img_arr,
    )
    wc.generate_from_text(string)

    #绘制
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')

    plt.savefig(resImageSrc,dpi=800,bbox_inches='tight',pad_inches=-0.1)

get_img('summary','./static/cloud.jpg','./static/cloudimg/summaryCloud.jpg')
