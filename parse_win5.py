import json
from collections import defaultdict
import csv
def main():
    with open('result.json', 'r') as json_file:
        win5_json = json.load(json_file)
    popular_count_dict = get_popular_count_list(win5_json['win5_data_list'])
    with open('win5_popular_count.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['人気','回数'])
        writer.writerow(['string', 'number'])

        for popular in range(1,19):
            writer.writerow([popular, popular_count_dict[str(popular)]])



def get_popular_count_list(win5_data_list):
    res_popular_count = defaultdict(int)
    for win5_data in win5_data_list:
        popular_list = win5_data['popular']
        for popular in popular_list:
            popular_str = str(popular)
            res_popular_count[popular_str]  += 1
    return res_popular_count



if __name__ == '__main__':
    main()
    
