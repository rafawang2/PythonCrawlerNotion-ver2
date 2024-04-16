import requests
from lxml import etree
import pandas as pd
import re
from random import randint
from time import sleep
from GetPageData import page_crawel
import os

def loading_bar(duration):
    total_ticks = 10
    for i in range(total_ticks + 1):
        progress = i / total_ticks
        bar = '#' * int(progress * 20)
        spaces = ' ' * (20 - len(bar))
        print(f'\r[{bar}{spaces}] {int(progress * 100)}%', end='', flush=True)
        sleep(duration / total_ticks)
    print()

def generate_author_url(keyword):   #輸入作者後產生作者頁面之連結
    link = "https://search.books.com.tw/search/query/cat/1/sort/1/v/1/page/1/spell/3/ms2/ms2_1/key/" + keyword + "#f_adv"
    print(link)
    return link

def generate_page_link(keyword,page):
    link = "https://search.books.com.tw/search/query/cat/all/sort/1/v/1/adv_author/1/spell/3/ms2/ms2_1/page/" + str(page) + "/key/" + keyword
    return link

def generate_book_url(bookID): #利用書本ID產生該書連結
    return "https://www.books.com.tw/products/" + bookID + "?sloc=main"

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
               "AppleWebKit/537.36 (KHTML, like Gecko)"
               "Chrome/63.0.3239.132 Safari/537.36"}

keyword=str(input("請輸入作者:"))
print("建立連結中...")
res = requests.get(generate_author_url(keyword),headers=headers)
if(res.status_code == requests.codes.ok):
    content = res.content.decode()  #解碼網頁
    html = etree.HTML(content)
    pages_cnt_list = html.xpath('/html/body/div/div/div/div/div/ul/li/select/option/text()')
    if(pages_cnt_list!=[]):
        pages_cnt = re.search(r'\d+', pages_cnt_list[0])
        pages_cnt = int(pages_cnt.group())
    else:
        pages_cnt = 1
    print(f'共{pages_cnt}頁')
    df = pd.DataFrame({'書名': [], '書本封面':[], 'ISBN': [], '作者':[], '出版社':[],'出版日期':[], '書本連結': []})
    for i in range(1,pages_cnt+1):
        page_link = generate_page_link(keyword,i)
        print(f'抓取第{i}頁資料中')
        df = pd.concat([df, page_crawel(page_link)], axis=0)
    
    print('所有書籍抓取完畢!')
    print(df)
    current_directory = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(os.path.join(current_directory, "作者csv")):
        os.makedirs(os.path.join(current_directory, "作者csv"))
    file_path = os.path.join(current_directory, "作者csv" , keyword + ".csv")

    df.to_csv(file_path,index=False,encoding='utf-8')
else:
    print('存取被拒')


