from urllib import request
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time
import re

CATEGORY = {'waku':1, 'kyaku':2, 'jockey':3, 'trainer':4, 'breed':5}
def main():
    race_dates = get_racedate_with_year(2020, False)
    for date in race_dates:
        kaisai_ids = get_kaisai_id_with_date(date)
        if kaisai_ids:
            for kaisai_id in kaisai_ids:
                url = get_source_url(date, kaisai_id)
                get_all_data_with_url(url)
            else:
                url = get_source_url(date)
                get_all_data_with_url(url)

def get_all_data_with_url(url):
    if not validate_url(url):
        return
    file_name, res = get_waku_with_url(url+'&category=1')
    res_kyaku = get_kyakushitu_with_url(url+'&category=2')
    res.append(res_kyaku)
    res_jockey = get_jockey_trainer_bleed_with_url(url+'&category=3')
    res.append(res_jockey)
    res_trainer = get_jockey_trainer_bleed_with_url(url+'&category=4')
    res.append(res_trainer)
    res_bleed = get_jockey_trainer_bleed_with_url(url+'&category=5')
    res.append(res_bleed[0:12])
    res.append(res_bleed[12:])
    df = pd.DataFrame(res).T
    df.columns = ['title', 'condition', 'ground', 'waku', 'kyakushitsu', 'jockey', 'trainer', 'father', 'grandpa']
    # df.to_csv('{}.csv'.format(file_name))
    race_date = url[-8:]
    file_name = race_date + file_name
    df.to_json('./json/{}.json'.format(file_name))
    print(file_name)

def validate_url(url):
    try:
        response = request.urlopen(url)
        return True
    except:
        return False
    
def get_waku_with_url(url):
    response = request.urlopen(url)
    soup = BeautifulSoup(response, 'html.parser')
    response.close()
    #レース会場
    stadium = soup.find(class_='RaceMainMenu').find('a').get_text()
    # print(stadium)
    #レース番号
    condition = [condition.get_text() for condition in  soup.find_all(class_='Condition')]
    # race_nums = [num.get_text() for num in soup.find_all(class_='Rank')]
    # print(race_nums)
    #レース名
    race_names = [race_name.get_text() for race_name in  soup.find_all(class_='Race_Name')]
    # print(race_names)
    grounds = [ground.get_text() for ground in  soup.find_all(class_='Txt_C')]
    # print(grounds)
    numbers = [num.get_text().split('\n')[1:4] for num in  soup.find_all(class_='Number')]
    date_info = soup.find(class_='TitleHeading').get_text()
    res = [race_names, condition, grounds, numbers]
    # res = pd.DataFrame([race_names,condition, grounds, numbers]).T
    file_name = date_info[1:-1].replace(' ', '-')
    file_name = file_name.split('-')[1:]
    file_name = '-'.join(file_name)
    return file_name, res

def get_kyakushitu_with_url(url):
    response = request.urlopen(url)
    soup = BeautifulSoup(response, 'html.parser')
    response.close()

    kyakushitsu = [num.get_text().replace('\n', '').replace(' ','').split('-') for num in  soup.find_all(class_='Number')]
    return kyakushitsu
    # res.to_csv('{}.csv'.format(file_name))

def get_jockey_trainer_bleed_with_url(url):
    response = request.urlopen(url)
    soup = BeautifulSoup(response, 'html.parser')
    response.close()
    jockeys = [a.get_text() for  a in soup.find_all(class_='Inner')]
    res = []
    for i in range(0, len(jockeys), 3):
        res.append(jockeys[i:i+3])
    return res


def get_racedate_with_year(year, skip=False):
    m = datetime.date.today().month if skip else 1
    months = [i for i in range(m,13)]
    days = [i for i in range(1,32)]
    res = []
    for month in months:
        for day in days:
            try:
                date = datetime.date(year, month, day)
                if date > datetime.date.today():
                    continue
                                           # 月曜開催 金曜開催
                if date.weekday() >=4 or date.weekday() == 0:
                    res.append('{:%Y%m%d}'.format(date))
            except ValueError:
                pass
    return res

def get_kaisai_id_with_date(date):
    base_url = 'https://racev3.netkeiba.com/top/tendency.html?'
    url = base_url + 'kaisai_date=' + date
    try:
        response = request.urlopen(url)
    except:
        # print('Not Found')
        return False
    soup = BeautifulSoup(response, 'html.parser')
    response.close()
    pat = r'[0-9]{10}'
    res = []
    for href in soup.find_all(class_='Tab_Normal'):
        tmp = re.search(pat, str(href.get('href')))
        if tmp:
            res.append(tmp.group())
    return res

def get_source_url(date, kaisai_id=None):
    base_url = 'https://racev3.netkeiba.com/top/tendency.html?'
    if kaisai_id:
        return '{}kaisai_id={}&kaisai_date={}'.format(base_url,kaisai_id, date)
    else :
        return '{}kaisai_date={}'.format(base_url, date)


if __name__ == '__main__':
    main()
    # get_all_data_with_url('https://racev3.netkeiba.com/top/tendency.html?kaisai_id=2020080107&kaisai_date=20200119')
    
