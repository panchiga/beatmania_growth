
# coding: utf-8

# # にでらせいちょうきろく
#
# KONAMIに税金を払うとダウンロードできるbeatmaniaの「スコアデータCSV」を使ってクリア以上の更新曲を記録して成長を可視化したい。
#
# 一応グラフも表示するようにしたけど成長して無いのでは…?って気持ちになってしまったので微妙かも…
#
# ## Directory
# ```
# ./
# - data/
#   - checked/
#   - result/
#     - growth.csv
#   - latest.csv
# - beatmania_growth_visualization.py
# ```
#

# get_ipython().magic('matplotlib inline')
import pandas as pd
import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt
import glob
import os

file_list = glob.glob("./data/20*.csv")
file_list.sort()
latest_file = "data/latest.csv"
growth_file = "data/result/growth.csv"

growth_df = pd.read_csv(growth_file)
growth_df = growth_df[['Title','Difficult','Level','Scere','PGreat','Great','MissCount','ClearType','ClearRate','PlayDate']]

# 連結済みのデータフレームで指定した列に差が有るもののIDリストを返す
def diff_df(df, difficult):
    cols = [" ミスカウント"," クリアタイプ"," EXスコア"]
    # cols = map(lambda item:difficult+item, cols)

    cols = [difficult+item for item in cols]

    # クリアタイプが"NO PLAY"ならスキップ
    skip_col = difficult + " クリアタイプ_x"
    skip_str = "NO PLAY"

    newly_list = []
    for i in df.index:
        if df.iloc[i][skip_col] == skip_str:
            continue
        for col in cols:
            # select merged df with column_name
            column_name_x = col + '_x'
            column_name_y = col + '_y'

            if df.iloc[i][column_name_x] != df.iloc[i][column_name_y]:
                newly_list.append(i)
                break

    return newly_list

# 難易度毎に抽出する
def extract_diff(df, merged_df, difficult):
    diff = df.iloc[diff_df(merged_df, difficult)]

    diff[['タイトル',difficult+' 難易度',
       difficult+' EXスコア', difficult+' PGreat', difficult+' Great', difficult+' ミスカウント',
       difficult+' クリアタイプ', difficult+' DJ LEVEL', '最終プレー日時']]

    diff = diff.rename(columns={
        'タイトル': 'Title',
        difficult+' 難易度':'Level',
        difficult+' EXスコア':'Scere',
        difficult+' PGreat':'PGreat',
        difficult+' Great':'Great',
        difficult+' ミスカウント':'MissCount',
        difficult+' クリアタイプ':'ClearType',
        difficult+' DJ LEVEL':'ClearRate',
        '最終プレー日時':'PlayDate'
    })
    diff["Difficult"] = difficult

    return diff

# 更新曲をNORMAL,HYPER,ANOTHER毎に取得
def fetch_growth(df,merged):
    col = "NORMAL"
    n_diff = extract_diff(df, merged,col)
    col = "HYPER"
    h_diff = extract_diff(df, merged,col)
    col = "ANOTHER"
    a_diff = extract_diff(df, merged,col)

    all_diff = pd.concat([n_diff,h_diff,a_diff])

    all_diff = all_diff[['Title','Difficult','Level','Scere','PGreat','Great','MissCount','ClearType','ClearRate','PlayDate']]
    all_diff['PlayDate'] = all_diff['PlayDate'].dt.date

    return all_diff

# main
for check_file in file_list:
    print(check_file)
    base_df = pd.read_csv(latest_file)
    after_df = pd.read_csv(check_file)

    date_col="最終プレー日時"
    after_df[date_col] = pd.to_datetime(after_df[date_col])
    base_df[date_col] = pd.to_datetime(base_df[date_col])

    #diff_df = after_df[~after_df["最終プレー日時"].isin(base_df["最終プレー日時"])]
    merged = pd.merge(after_df, base_df,on='タイトル',how='outer')

    delta_growth = fetch_growth(after_df, merged)
    # print(delta_growth)
    add_growth = delta_growth.query('ClearType != "FAILED"').sort_values(by=["PlayDate","Level"]).reset_index(drop=True)

    growth_df = pd.concat([growth_df, add_growth])

    # after_dfをcheckedにコピーして名前をlatest.csvにして上書き
    after_df.to_csv('data/checked/'+check_file.split('/')[-1])
    after_df.to_csv(latest_file)
    os.remove(check_file)

growth_df.reset_index(drop=True).to_csv(growth_file)

# 弐寺をプレイした日に更新した曲をレベル毎にカウント
growth_pivot = growth_df.pivot_table(values = ['Difficult'],
                      index = ['PlayDate'],
                      columns = ['Level'],
                      aggfunc = 'count',
                      fill_value=0
                     )
# growth_pivot

# グラフの保存
plt.figure()

# 濃いほど強い
growth_pivot.plot(kind='area', colormap='Reds',figsize=(18, 8))

plt.savefig('data/result/mygrowth.png')
plt.close('all')
