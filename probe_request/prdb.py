import pandas as pd
import numpy as np
import re

data = pd.read_csv("/Users/kidago/Documents/probe_request/2023_4_19_osaka_shinosaka_w.csv",header=0)

#InfoからSSIDとSNを取り出す
data["Info"] = data["Info"].str.strip("Probe Request, SN=")
data["SN"] = data["Info"].str.extract(r'(\d+)').astype(int)
data["Info"] = data["Info"].str.replace('\d+', '', regex=True)
data["Info"] = data["Info"].str.strip(", FN=0, Flags=........C, SSID=")
data["Info"] = data["Info"].str.strip('"')

print(data)

#同じMACアドレスでグループ分け
#group1 = data.groupby("Source")
#group1.apply(print)
data["mac_num"] = data["Source"].factorize()[0]
data["SSID_num"] = data["Info"].factorize()[0]
# MACアドレスでグループ化
grouped = data.groupby("Source")

# 各グループのSSIDをまとめて操作
for mac_address, group in grouped:
    ssid_list = group["Info"].tolist()
    # ここでSSIDリストを操作する
    print(f"MACアドレス: {mac_address}")
    print(f"SSIDリスト: {ssid_list}")
    print("")


#シーケンス番号で連続しているものでグループ分け

#グループ分けしたものをSSIDの組み合わせの一致割合の高いものでグループ分け

