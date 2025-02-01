import json
import sys,os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from collections import defaultdict
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))
from utils.json_reader import JSONFileHandler

def main():
    if len(sys.argv) < 2:
        print('Need argument for target year')
        exit(1)
    target_year =  sys.argv[1]
    target_dir = './data/' + target_year
    result_json_handler = JSONFileHandler('{}/win5_result.json'.format(target_dir))
    result_detail_json_handler = JSONFileHandler('{}/win5_result_detail.json'.format(target_dir))
    result_json = result_json_handler.read_json()
    result_detail_json = result_detail_json_handler.read_json()
    
    populuar_sum = []
    jockey_win_nums = defaultdict(int)
    for data in result_json['win5_data_list']:
        print('Start target win5 ' + data['win5_id'])
        win5_detail_dict = result_detail_json['win5_data_race_detail']
        for race_num in range(1,6): 
            target_data = next((item for item in win5_detail_dict if item["race_id"] == data['win{}_race_id'.format(race_num)]), None)
            jockey_win_nums[target_data['win_horse_jockey']]+=1
        populuar_sum.append(sum(data['popular']))
    sorted_jockey_win_nums = sorted(jockey_win_nums.items(),  key = lambda item : item[1], reverse=True)

    jockey_names = [i[0] for i in sorted_jockey_win_nums]
    jockey_wins = [i[1] for i in sorted_jockey_win_nums]
    min_win_num = min(jockey_wins) if min(jockey_wins) > 1 else 0
    filtered_data = [(x_val, y_val) for x_val, y_val in zip(jockey_names,jockey_wins) if y_val > min_win_num]

    # フィルタリングされたデータから新しいxとyを作成
    jockey_names_filterd, jockey_wins_filtered = zip(*filtered_data)
    fig = go.Figure(
            data=go.Bar(
                x=jockey_names_filterd,
                y=jockey_wins_filtered,
                name="勝利数",
                marker=dict(color=jockey_wins,
                    colorscale=px.colors.sequential.Greens)
            )
        )
    fig.update_layout(
        yaxis=dict(
            title=dict(text="WIN5対象レース勝利数"),
            side="left"
        ),
        # plot_bgcolor='Black'
    )
    # fig.show()
    output_dir = './fig/{}/'.format(target_year)
    os.makedirs(output_dir, exist_ok=True)
    output_path = output_dir + 'win5_jockey_win_plotly.json'
    fig.write_json(output_path)
    # fig.write_html("./win5_jockey_win.html", full_html=False,include_plotlyjs=False)
    



if __name__ == '__main__':
    main()