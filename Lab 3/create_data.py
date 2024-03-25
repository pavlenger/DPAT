import pandas as pd
import urllib.request
from os import listdir, walk
from datetime import datetime

DIRECTORY = 'CSV_Files/'
URL = ('https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={'
       '}&year1=1981&year2=2020&type=Mean')
INDEXES = {1: 22, 2: 24, 3: 23, 4: 25, 5: 3, 6: 4, 7: 8, 8: 19, 9: 20, 10: 21, 11: 9, 13: 10, 14: 11, 15: 12,
           16: 13,
           17: 14, 18: 15, 19: 16, 21: 17, 22: 18, 24: 1, 25: 2, 26: 7, 27: 5, 28: 6}


def download():
    for province_id in range(1, 29):
        url = URL.format(province_id)
        wp = urllib.request.urlopen(url)
        text = wp.read()
        now = datetime.now()
        date_and_time_time = now.strftime("%d-%m-%Y_%H-%M-%S")
        out = open(DIRECTORY + 'NOAA_ID' + str(province_id) + '_' + date_and_time_time + '.csv', 'wb')
        out.write(text)
        out.close()
        # print('File for ' + str(province_id))
    print('Success')


def func():
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
    i = 1
    df_list = []
    for (dirpath, dirnames, filenames) in walk(DIRECTORY):
        for filename in filenames:
            df = pd.read_csv(DIRECTORY + filename, header=1, names=headers)
            df.at[0, 'Year'] = df.at[0, 'Year'][9:]
            df = df.drop(df.index[-1])
            df = df.drop(df.loc[df['VHI'] == -1].index)
            df = df.drop('empty', axis=1)
            id = int(filename.split("_")[1][2:])
            # print(filename)
            df['area'] = id
            # print(id)
            i += 1
            df_list.append(df)
    df = pd.concat(df_list)
    df.replace({'area': INDEXES}, inplace= True)
    print(df)
    df.to_csv('data.csv')
    return df


# download()
func()
