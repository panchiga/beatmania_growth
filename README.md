# beatmania_growth

## 環境
- python 3.6
- pandas 0.20.1
- matplotlib 2.0.2

## 使い方
1. 公式サイトからDLできる`スコアデータCSV`のファイル名を、ダウンロードした日に変更して`data`フォルダに格納(例:`20180511.csv`)
2. `python beatmania_growth_visualization.py`を実行
3. 更新した曲が`data/result/growth.csv`に追記されていき、そのグラフが`data/result/growth.png`に保存される
4. 確認した`スコアデータCSV`は`data/checked/`以下に勝手に移動する

BeatmaniaスコアデータCSVを使って成長を実感しよう!
