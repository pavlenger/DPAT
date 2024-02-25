import pandas as pd
import urllib.request
from datetime import datetime
from constants import *
from os import walk


def download_file(province_id):
    """
download file from database on site
    :param province_id: id of province
    """
    url = URL.format(province_id)
    wp = urllib.request.urlopen(url)
    text = wp.read()
    now = datetime.now()
    date_and_time_time = now.strftime("%d-%m-%Y_%H-%M-%S")
    out = open(DIRECTORY + 'NOAA_ID' + str(province_id) + '_' + date_and_time_time + '.csv', 'wb')
    out.write(text)
    out.close()


def create_frame(directory):
    """
create dataframe from all files in directory
    :param directory: path to directory
    :return: dataframe with all files in directory
    """
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
    i = 1
    df_list = []
    for (dirpath, dirnames, filenames) in walk(DIRECTORY):
        for filename in filenames:
            df = pd.read_csv(directory + filename, header=1, names=headers)
            df = df.drop(df.loc[df['VHI'] == -1].index)
            df['area'] = i
            i += 1
            df_list.append(df)
    return pd.concat(df_list)


def change_indexes(df):
    """
change indexes of areas in dataframe    :param df:  with all files
    """
    df.replace({'area': INDEXES}, inplace=True)


def procedure_1(df, year, province_n):
    """
display min and max values of VHI by province id and year
    :param df: dataframe with all files
    :param year: year of data
    :param province_n: province id of data
    """
    df_new = df[(df.area == province_n) & (df.VHI != -1) & (df.Year.astype(str) == str(year))]['VHI']
    print('For ' + str(year) + ' and the province ' + str(province_n) + ':')
    print('Min: ' + str(df_new.min()))
    print('Max: ' + str(df_new.max()))


def procedure_2(df, province_n):
    """
display years with extreme drought by province id
    :param df: dataframe with all files
    :param province_n: province id of data
    """
    df_drought = df[(df["area"] == province_n) & (df.VHI <= 15) & (df.VHI != -1)]
    list_from_ds = list(df_drought.Year)
    years = []
    [years.append(item) for item in list_from_ds if item not in years]
    print('For the province ' + str(province_n) + ' extreme drought is in:')
    print('Years: ' + ' '.join(years))


def procedure_3(df, province_n):
    """
display years with moderate drought by province id
    :param df: dataframe with all files
    :param province_n: province id of data
    """
    df_drought = df[(df["area"] == province_n) & (df.VHI <= 35) & (df.VHI > 15) & (df.VHI != -1)]
    list_from_ds = list(df_drought.Year)
    years = []
    [years.append(item) for item in list_from_ds if item not in years]
    print('For the province ' + str(province_n) + ' moderate drought is in:')
    print('Years: ' + ' '.join(years))


for province_n in range(1, 29):
    download_file(province_n)

df = create_frame(DIRECTORY)
change_indexes(df)

procedure_1(df, 1990, 3)
procedure_2(df, 3)
procedure_3(df, 3)
