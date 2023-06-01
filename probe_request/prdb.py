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
list1 = np.zeros((100,2))
tmp = 0
p = 0
#先頭がMACアドレスでその後にSSIDが複数続く配列を作る
while True:
    if tmp == data.shape[0]:
        break

    tmp2 = 0

    for t in list1:
        if list1[tmp2][0] == data.loc[tmp,"Source"]:
            print("b")
            list1[list1.index(data.loc[tmp,"Source"])].append(data.loc[tmp,"Info"])
            break
        elif all(list1[tmp2]):
            print("b")
            list1[p] = [data.loc[tmp,"Source"],data.loc[tmp,"Info"]]
            p = p + 1
            break
        
        tmp2 = tmp2 + 1
            
    tmp = tmp + 1

print(list1)
#シーケンス番号で連続しているものでグループ分け

#グループ分けしたものをSSIDの組み合わせの一致割合の高いものでグループ分け

