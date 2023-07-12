import pandas as pd
import hashlib
from tkinter import filedialog
import tkinter as tk
import tkinter.filedialog as fd

def anonymize_mac_address(mac_address):
    #mac_address = mac_address.str.strip(":")

    # 後半3桁を切り出す
    last_three_digits = mac_address[-8:]

    # ハッシュ化
    hashed = hashlib.sha256(last_three_digits.encode()).hexdigest()

    # 匿名化されたMACアドレスを生成
    anonymized_mac_address = mac_address[:-8] + hashed

    return anonymized_mac_address

typ = [('テキストファイル','*.csv')]
dir = 'C:\\pg'
fle = filedialog.askopenfilename(filetypes = typ, initialdir = dir)


data = pd.read_csv(
    fle, header=0
)

print(data)

# InfoからSSIDとSNを取り出す
data["Info"] = data["Info"].str.strip("Probe Request, SN=")
data["SN"] = data["Info"].str.extract(r"(\d+)").astype(int)
data["Info"] = data["Info"].str.replace("\d+", "", regex=True)
data["Info"] = data["Info"].str.strip(", FN=0, Flags=........C, SSID=")
data["Info"] = data["Info"].str.strip('"')

for index,mac in data.iterrows():
    data.at[index,"Source"] = anonymize_mac_address(mac["Source"])
    #print(mac)

print(data)

save = input("保存するファイル名を入力してください")

data.to_csv("/Users/kidago/Documents/probe_request/"+save+".csv", index=False)

