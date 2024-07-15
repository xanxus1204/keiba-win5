import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

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
        
        

def main():

    with open('./result.json' , 'r') as jsonf:
        result_json = json.load(jsonf)
    x = len(result_json['win5_data_list'])
    x_axis = [i for i  in range(1,x+1)]

    populuar_sum = []
    refunds = []
    refunds_kanji = []
    for data in result_json['win5_data_list']:
        print(data['win5_id'])
        refund = data['refund']
        refunds_kanji.append(refund)
        refunds.append(kanji_yen_to_number(refund))
        # print(data['race_name'])
        # print(data['popular'])
        populuar_sum.append(sum(data['popular']))
        # print(data['number'])
        # print(data['bracket'])


    fig = go.Figure(
        data=go.Bar(
            x=x_axis,
            y=populuar_sum,
            name="人気の和",
            marker=dict(color="green"),
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
            title=dict(text="人気の和"),
            side="left"
        ),
        yaxis2=dict(
            title=dict(text="払戻金"),
            side="right",
            overlaying="y",
            tickmode="sync",
            type='log'
        ),
    )
    # fig.update_yaxes(type='log')
    fig.show()
    # fig.write_html("./index.html", full_html=False,include_plotlyjs=False)



if __name__ == '__main__':
    main()