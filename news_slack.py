import pandas as pd
import numpy as np
import sqlite3

import requests
import json
import os
from bs4 import BeautifulSoup as bs
import time


def make_today_news(search):
    url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={}'
    headers = {'Referer':'https://www.naver.com'
                   ,'upgrade-insecure-requests':'1'
                   ,'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}
    
    r = requests.get(url.format(search), headers = headers)
    soup = bs(r.text, "lxml")
    htmls = soup.select("dl > dt > a") 

    today_news = []
    for html in htmls:
        today_news.append((html.get('href'), html.get('title')))

    today_news = pd.DataFrame(today_news, columns=['url', 'title'])
    today_news = today_news[today_news['title'].notnull()]   # 제목이 없는 url 삭제
    
    stop_words = '빅데이터MSI|시장심리'   # | 구분자로 계속 제외 단어 넣기 
    bools = ~today_news['title'].str.contains(stop_words, regex=True)
    today_news = today_news[bools]
    return today_news   

def make_all_news(today_news):
    try: 
        all_news = pd.read_sql("select * from all_news", con)
    except:
        print("데이터가 없네요. 현재 데이터를 넣습니다.")    
        today_news.to_sql('all_news', con, if_exists='append', index=False)  # index=False 인덱스는 넣지 않는다. 
        all_news = pd.read_sql("select * from all_news", con)
    return all_news

def check_dup_url(u, ser):
    return ser.apply(lambda x: True if u == x else False).any()  # 한건이라도 겹치면, True 반환

def send_slack(msg):
    webhook_url = "YOUR_SLACK_URL"
    content = msg
    payload = {"text": content}
    requests.post(
        webhook_url, data=json.dumps(payload),
        headers={'Content-Type': 'application/json'})
 

if __name__ == '__main__':
    
    con = sqlite3.connect("news_list.db")
    
    today_news = make_today_news('금융빅데이터')
    all_news = make_all_news(today_news)        
    
    for i, row in today_news.iterrows():
        if check_dup_url(row.url, all_news['url']):   # 중복 있으면
            pass
        else:
            msg = (row.title + '\n' + row.url)  # 제목+URL로 구성
            send_slack(msg)
            df_add = pd.DataFrame({'url':[row.url], 'title':[row.title]})
            df_add.to_sql('all_news', con, if_exists='append', index=False)
            break    