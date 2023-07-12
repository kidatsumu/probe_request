import pandas as pd
import numpy as np
import re
import itertools
from tkinter import filedialog
from collections import OrderedDict
import tkinter as tk
import tkinter.filedialog as fd

def listify(column):
    return list(set(column))

#ファイルの選択
typ = [('CSVファイル','*.csv')]
dir = 'C:\\pg'
fle = filedialog.askopenfilename(filetypes = typ, initialdir = dir)

data = pd.read_csv(
    fle, header=0
)

# InfoからSSIDとSNを取り出す
#data["Info"] = data["Info"].str.strip("Probe Request, SN=")
#data["SN"] = data["Info"].str.extract(r"(\d+)").astype(int)
#data["Info"] = data["Info"].str.replace("\d+", "", regex=True)
#data["Info"] = data["Info"].str.strip(", FN=0, Flags=........C, SSID=")
#data["Info"] = data["Info"].str.strip('"')

data["mac_num"] = data["Source"].factorize()[0]
data["ssid_num"] = data["Info"].factorize()[0]

grouped = data.groupby("Source")

ssid_list = grouped["Info"].apply(listify).reset_index()

ssid_list["Info_Len"] = ssid_list["Info"].apply(len)

ssid_list = ssid_list.sort_values("Info_Len",ascending=False).reset_index()

print(ssid_list)

save = input("保存するファイル名を入力してください：")

ssid_list.to_csv("/Users/kidago/Documents/probe_request/"+save+".csv")
