import pandas as pd
from collections import defaultdict
import re
import pathlib
import matplotlib.pyplot as plt
import os
ALL_PLACES = ('札幌', '函館', '福島', '新潟', '中山', '中京','京都', '阪神', '小倉', '東京')
def main():
    file_path = './json'
    divide_to_places = divide_to_place(file_path)
    divide_to_holds = divide_to_hold(divide_to_places)
    # print(divide_to_holds['京都'][1])
    for place in divide_to_holds.keys():
        holds = divide_to_holds[place]
        if len(holds[0]) == 0:
            continue
        for i in range(len(holds)):
            for ground in ('芝', 'ダ'):
                num_1st = get_number_1st(holds[i], ground)
                img_name = 'img/Number-{}-{}-{}.png'.format(place, i+1, ground)
                x = [i[0] for i in num_1st]
                y = [i[1] for i in num_1st]
                plt.xticks([i+1 for i in range(max(x))])
                plt.bar(x, y)
                plt.savefig(img_name)
                plt.clf()


    for place in divide_to_holds.keys():
        holds = divide_to_holds[place]
        for i in range(len(holds)):
            for ground in ('芝', 'ダ'):
                kyaku_1st = get_kyaku_1st(holds[i], ground)
                img_name = 'img/Kyaku-{}-{}-{}.png'.format(place, i+1, ground)
                x = [i[0] for i in kyaku_1st]
                y = [i[1] for i in kyaku_1st]
                plt.bar(x, y)
                plt.savefig(img_name)
                plt.clf()
        

def divide_to_place(folder):
    p = pathlib.Path(folder)
    data = {}
    for r in ALL_PLACES:
        data[r] = []
    for json_file in p.glob('*.json'):
        json_file = str(json_file)
        place = os.path.basename(json_file)[8:10]
        if place in data:
            data[place].append(json_file)
    return data


def divide_to_hold(race_by_place):
    res = {}
    for p in ALL_PLACES:
        res[p] = []
    for place in race_by_place.keys():
        hold_counts = []
        before = 0
        tmp = []
        for js in sorted(race_by_place[place]):
            day_pat = re.search(r'-(\d{1,2})', js)
            day = int(day_pat.groups()[0])
            if day < before:
                hold_counts.append(tmp)
                tmp = []
                tmp.append(js)
                before = 0
            else:
                before = day
                tmp.append(js)
        else:
            hold_counts.append(tmp)
        res[place] = hold_counts
    return res


def get_number_1st(race_by_hold, ground):
    res = defaultdict(int)
    for json_file in race_by_hold:
        df = pd.read_json(json_file)
        if df.isnull().values.sum() != 0:
            continue
        df = df[df['condition'].str.contains(ground)]
        for _, row in df.iterrows():
            waku = row[3]
            if waku[0] == '':
                print('Incomplete data')
                return sorted(res.items(), key=lambda x: x[0])
            res[int(waku[0])] += 1
    return sorted(res.items(), key=lambda x: x[0])


def get_kyaku_1st(race_by_hold, ground):
    res = defaultdict(int)
    for json_file in race_by_hold:
        df = pd.read_json(json_file)
        if df.isnull().values.sum() != 0:
            continue
        df = df[df['condition'].str.contains(ground)]
        for _, row in df.iterrows():
            kyaku = row[4]
            if kyaku[0] == '':
                print('Incomplete data')
            res[kyaku[0]] += 1
    return sorted(res.items(), key=lambda x: x[0])
if __name__ == '__main__':
    main()
    
