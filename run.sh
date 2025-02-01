#!/bin/bash

python3 get_win5.py 2025
sleep 3
python3 get_win5_detail_by_race_id.py 2025
sleep 3
python3 -m fig.make_win5_jockey 2025
python3 -m fig.make_return_odds_sum 2025


cp -r /home/equinox1204/script/keiba-win5/fig /home/equinox1204/win5-minimum.com/public_html/html/
rm /home/equinox1204/win5-minimum.com/public_html/html/fig/*.py