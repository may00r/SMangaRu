import requests
import os
import re
from bs4 import BeautifulSoup as bs

def save_manga(i, manga_path):
    IMG_URL = '{0}'.format(arrUrl[i])
    IMG_NAME = IMG_URL.split('/')[-1]
    r = requests.get(IMG_URL, stream=True)
    with open(manga_path+IMG_NAME, 'bw') as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)

mangaName = 'annarasumanara'
volNum = 1
chapterNum = 1
html = requests.get('http://readmanga.me/{0}/vol{1}/{2}'.format(mangaName, volNum, chapterNum))

soup = bs(html.text, 'html.parser')
imgDiv = soup.find('div', class_='pageBlock container reader-bottom')#.find_all('script')[1]
imgScr = ''.join(re.findall(r'rm_h.init.+', imgDiv.text))
result = re.findall(r'http://\w+.\w+.\w+/', imgScr)
resFindUrl = re.findall(r'".+?"', imgScr)

chapterCount = len(result)

resUrl = []
for i in range(0, chapterCount):
    resUrl.append(''.join(re.findall(r'[^"]', resFindUrl[i])))

manga_path = 'G://manga/{0}/{1}/{2}/'.format(mangaName, volNum, chapterNum)
if not os.path.exists(manga_path):
    os.makedirs(manga_path)

arrUrl = []
for i in range(0, chapterCount):
    arrUrl.append(result[i]+resUrl[i])
    print(arrUrl[i]) # -> выводит все ссылки
    save_manga(i, manga_path)
print(len(arrUrl))

