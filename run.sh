#!/bin/bash

python3 get_win5.py
sleep 3
python3 get_win5_detail_by_race_id.py
sleep 3
python3 ./fig/make_win5_jockey.py

cp /home/equinox1204/script/keiba-win5/fig/win5_jockey_win_plotly.json /home/equinox1204/win5-minimum.com/public_html/html/fig/