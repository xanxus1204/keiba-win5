import time
import json
import re
from bs4 import BeautifulSoup
from urllib import request
RESULT_INPUT_PATH = './data/win5_result.json'
RESULT_OUTPUT_PATH = './data/win5_result_detail.json'
def main():
    with open(RESULT_INPUT_PATH , 'r') as jsonf:
        result_json = json.load(jsonf)
    results = []
    for data in result_json['win5_data_list']:
        time.sleep(0.1)
        for i in range(1,6):
            res_dict = get_one_race_with_race_id(data['win{}_race_id'.format(i)])
            results.append(res_dict)
    res_dict = {"win5_data_race_detail": results}

    with open(RESULT_OUTPUT_PATH, 'w') as json_file:
        json.dump(res_dict, json_file)


def get_one_race_with_race_id(race_id):
    url = 'https://race.netkeiba.com/race/result.html?race_id=' + race_id
    print(url)
    response = request.urlopen(url)
    htmlsource = BeautifulSoup(response, 'html.parser')
    win_horse_data = htmlsource.find_all(class_='HorseList')
    win_horse_age = win_horse_data[0].find(class_='Lgt_Txt Txt_C').get_text().lstrip().rstrip()
    win_horse_jockey_weight = win_horse_data[0].find(class_='JockeyWeight').get_text()
    win_horse_jockey = win_horse_data[0].find(class_='Jockey').get_text().lstrip().rstrip()
    win_horse_time = win_horse_data[0].find(class_='RaceTime').get_text()
    win_horse_odds = win_horse_data[0].find(class_='Odds Txt_R').get_text().lstrip().rstrip()
    win_horse_trainer = win_horse_data[0].find(class_='Trainer').get_text().rstrip()
    win_horse_weight = win_horse_data[0].find(class_='Weight').get_text().lstrip()
    race_conditions = htmlsource.find_all(class_='RaceData01')[0].get_text()
    distance_pat = r'\D\d{4}'
    race_course_track = re.search(distance_pat, race_conditions).group()
    race_ground_type = race_course_track[0:1]
    race_distance = race_course_track[1:]
    print(race_ground_type)
    ground_cond_pat = r'馬場:(\D)'
    race_ground_condition = re.search(ground_cond_pat, race_conditions).groups()[0]
    race_programs = htmlsource.find_all(class_='RaceData02')[0].get_text()
    # print(race_conditions)
    print(race_distance)
    # print(race_programs.split('\n'))
    race_handi_type = race_programs.split('\n')[8]
    race_horse_count = race_programs.split('\n')[9].rstrip('頭')
    race_info =  htmlsource.find('title').text
    race_grade_pat = r'\((.*?)\)'
    race_grade = re.search(race_grade_pat, race_info).groups()[0]
    print(race_grade)

    # print(win_horse_age)
    # print(win_horse_jockey_weight)
    # print(win_horse_jockey)
    # print(win_horse_time)
    # print(win_horse_odds)
    # print(win_horse_trainer[0:2])
    # print(win_horse_trainer[2:])
    # print(win_horse_weight)
    res_dict = {"race_id": race_id,
                "win_horse_age": win_horse_age,
                "win_horse_jockey_weight": win_horse_jockey_weight,
                "win_horse_jockey": win_horse_jockey,
                "win_horse_time": win_horse_time,
                "win_horse_odds": win_horse_odds,
                "win_horse_home_center": win_horse_trainer[0:2],
                "win_horse_trainer": win_horse_trainer[2:],
                "win_horse_weight": win_horse_weight,
                "race_ground_type": race_ground_type,
                "race_grade": race_grade,
                "race_distance": race_distance,
                "race_ground_condition": race_ground_condition,
                "race_handi_type": race_handi_type,
                "race_horse_count" : race_horse_count
    }
    # print(res_dict)
    return res_dict


if __name__ == '__main__':
    main()
    # get_one_race_with_race_id('202408010111') #芝レース
    # get_one_race_with_race_id('202406030410') #ダートレース
    # get_one_race_with_race_id('202409010811') #G2レース
