import json
import plotly.graph_objects as go
import plotly.express as px
def main():

    with open('./data/win5_result.json' , 'r') as jsonf:
        result_json = json.load(jsonf)
    with open('./data/win5_result_detail.json' , 'r') as jsonf:
        result_detail_json = json.load(jsonf)
      
    odds_sum = []
    refunds = []
    refunds_kanji = []
    for data in result_json['win5_data_list']:
        print('Start target win5 ' + data['win5_id'])
        refund = data['refund']
        win5_detail_dict = result_detail_json['win5_data_race_detail']
        odds_5race_sum = 0
        for race_num in range(1,6): 
            target_data = next((item for item in win5_detail_dict if item["race_id"] == data['win{}_race_id'.format(race_num)]), None)
            odds_5race_sum += float(target_data['win_horse_odds'])
        odds_sum.append(round(odds_5race_sum,1))
        refunds_kanji.append(refund)
        refunds.append(kanji_yen_to_number(refund))

    x = len(result_json['win5_data_list'])
    x_axis = [i for i  in range(1,x+1)]

    fig = go.Figure(
            data=go.Bar(
                x=x_axis,
                y=odds_sum,
                name="オッズの和",
                marker=dict(color="green"),
                hovertext=odds_sum
            )
        )

    fig.add_trace(
        go.Scatter(
            x=x_axis,
            y=refunds,
            yaxis="y2",
            name="払戻金",
            marker=dict(color="crimson"),
            hovertext=refunds_kanji
        )
    )
    fig.update_layout(
        legend=dict(orientation="h"),
        yaxis=dict(
            title=dict(text="オッズの和"),
            side="left"
        ),
        yaxis2=dict(
            title=dict(text="払戻金"),
            side="right",
            overlaying="y",
            # tickmode="sync",
            type='log',
            tickvals=[100_000 ,3_000_000, 10_000_000, 100_000_000, 400_000_000, 600_000_000]
        )
    )
    # fig.update_yaxes(type='log')
    # fig.show()
    output_path = './fig/win5_return_odds_sum.json'
    # fig.write_html("./win5_jockey_win.html", full_html=False,include_plotlyjs=False)
    fig.write_json(output_path)

def kanji_yen_to_number(kanji_yen):
    oku = 0
    man = 0
    en = 0
    if '億' in kanji_yen:
        temp = kanji_yen.split('億')
        oku = int(temp[0]) * 100000000
        kanji_yen = temp[1]
    if '万' in kanji_yen:
        temp = kanji_yen.split('万')
        man = int(temp[0]) * 10000
        kanji_yen = temp[1] 
    en = int(kanji_yen.rstrip('円'))
    res = oku + man + en
    return res
        
        

if __name__ == '__main__':
    main()