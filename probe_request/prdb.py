import pandas as pd
import numpy as np
import re
import itertools

def calculate_match_rate(group1, group2):
    common_elements = set(group1) & set(group2)
    match_rate = len(common_elements) / max(len(group1), len(group2))
    return match_rate

data = pd.read_csv("/Users/kidago/Documents/probe_request/2023_4_19_osaka_shinosaka_w.csv",header=0)

#InfoからSSIDとSNを取り出す
data["Info"] = data["Info"].str.strip("Probe Request, SN=")
data["SN"] = data["Info"].str.extract(r'(\d+)').astype(int)
data["Info"] = data["Info"].str.replace('\d+', '', regex=True)
data["Info"] = data["Info"].str.strip(", FN=0, Flags=........C, SSID=")
data["Info"] = data["Info"].str.strip('"')

#print(data)

#同じMACアドレスでグループ分け
#group1 = data.groupby("Source")
#group1.apply(print)
data["mac_num"] = data["Source"].factorize()[0]
data["SSID_num"] = data["Info"].factorize()[0]

print(data)
# MACアドレスでグループ化
grouped = data.groupby("Source")
grouped_ssid = list(grouped["SSID_num"])  # リストに変換する


threshold = 0.6  # 一致率の閾値
grouped_matches = []  # 一致率の高いグループ同士をまとめるリスト

# グループ同士の一致率を比較して、閾値を超える場合は同じグループに追加
for group1, group2 in itertools.combinations(grouped_ssid, 2):
    match_rate = calculate_match_rate(group1, group2)
    unique_elements = set(group1 + group2)
    if match_rate >= threshold and len(unique_elements) > 1:
        # 一致率が閾値以上であり、かつ組み合わせの中身が1種類以上ある場合、既存のグループに追加するか、新しいグループとして追加する
        for matches in grouped_matches:
            if group1 in matches or group2 in matches:
                matches.add(group1)
                matches.add(group2)
                break
        else:
            grouped_matches.append({group1, group2})

for group in grouped_matches:
    print(group)



# 各グループのSSIDをまとめて操作
#for mac_address, group in grouped:
    #ssid_list = group["Info"].tolist()
    # ここでSSIDリストを操作する
    #print(f"MACアドレス: {mac_address}")
    #print(f"SSIDリスト: {ssid_list}")
    #print("")

    #other_data = group.drop_duplicates(subset="Info", keep="first")

    # 重複を解消したSSIDリストを作成
    #unique_ssid_list = list(set(ssid_list))

#print(unique_ssid_list)

#シーケンス番号で連続しているものでグループ分け

#グループ分けしたものをSSIDの組み合わせの一致割合の高いものでグループ分け

