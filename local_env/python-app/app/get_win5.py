import re,datetime
import json
from bs4 import BeautifulSoup
from urllib import request


def main():
    this_year = datetime.datetime.now().year
    win5_url =  'https://race.netkeiba.com/top/win5_results.html?select=win5_results&year={}'.format(this_year)
    response = request.urlopen(win5_url)
    htmlsource = BeautifulSoup(response, 'html.parser')
    win5s = htmlsource.find_all(class_='WIN5_RaceListBox')
    res_list = []
    for win5 in win5s:
        # print(win5)
        win5_info = str(win5.find(class_='Win5RaceName')).split('\n')
        if len(win5_info) > 1:
            date_pat = r'[0-9]{8}'
            # 日付取得
            win5_date = win5_info[1]
            win5_date = re.search(date_pat, win5_date).group()
            win5_title = win5_info[2]
            title_pat = r'<span>(.+?)</span>'
            #レース名
            win5_title = re.search(title_pat, win5_title).groups()[0]
            win5_number_html = str(win5.find(class_='Win5_UmabanWrap'))
            
            #馬番
            num_pat = r'>(\d+)</li>'
            win5_number = re.findall(num_pat, win5_number_html)
            win5_number = [int(num) for num in win5_number]
            #枠
            waku_pat = r'Waku(\d+)'
            win5_waku = re.findall(waku_pat, win5_number_html)
            win5_waku = [int(waku) for waku in win5_waku]
            #人気
            win5_ninki_html = str(win5.find(class_='Win5_NinkiWrap'))
            ninki_pat = r'>(\d+)人気</span>'
            win5_ninki = re.findall(ninki_pat, win5_ninki_html)
            win5_ninki = [int(ninki) for ninki in win5_ninki]
            #払い戻し
            win5_pay_back_html = win5.find(class_='Win5_UmabanWrap')


            
            win5_dict = {"race_id": win5_date,
                         "race_name": win5_title,
                         "number": win5_number, 
                         "popular": win5_ninki,
                         "bracket": win5_waku}
            # print(win5_dict)
            res_list.append(win5_dict)
            # print('{},{},{},{}'.format(win5_date, win5_title, win5_number,win5_ninki))

    res_dict = {"win5_data_list" : res_list}
    json.dumps(res_dict)             
    with open('result.json', 'w') as json_file:
        json.dump(res_dict, json_file)
    # print(sorted(res.items(), key=lambda x: x[0]))


if __name__ == '__main__':
    main()
    
