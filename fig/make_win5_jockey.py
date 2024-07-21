import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from collections import defaultdict
def main():

    with open('./data/win5_result.json' , 'r') as jsonf:
        result_json = json.load(jsonf)
    with open('./data/win5_result_detail.json' , 'r') as jsonf:
        result_detail_json = json.load(jsonf)
      
    populuar_sum = []
    odds_sum = []
    jockey_win_nums = defaultdict(int)
    for data in result_json['win5_data_list']:
        print('Start target win5 ' + data['win5_id'])
        win5_detail_dict = result_detail_json['win5_data_race_detail']
        odds_5race_sum = 0
        for race_num in range(1,6): 
            target_data = next((item for item in win5_detail_dict if item["race_id"] == data['win{}_race_id'.format(race_num)]), None)
            jockey_win_nums[target_data['win_horse_jockey']]+=1
            odds_5race_sum += float(target_data['win_horse_odds'])
        odds_sum.append(odds_5race_sum)
        populuar_sum.append(sum(data['popular']))
    sorted_jockey_win_nums = sorted(jockey_win_nums.items(),  key = lambda item : item[1], reverse=True)

    jockey_names = [i[0] for i in sorted_jockey_win_nums]
    jockey_wins = [i[1] for i in sorted_jockey_win_nums]

    filtered_data = [(x_val, y_val) for x_val, y_val in zip(jockey_names,jockey_wins) if y_val > 1]

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
    output_path = './fig/win5_jockey_win_plotly.json'
    # fig.write_html("./win5_jockey_win.html", full_html=False,include_plotlyjs=False)
    fig.write_json(output_path)



if __name__ == '__main__':
    main()