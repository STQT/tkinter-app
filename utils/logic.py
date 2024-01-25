import time

import pandas as pd
from collections import Counter

from utils.functions import del_nan


def on_button_click(label):
    label.config(text="Нажата кнопка!")


def clean_data_from_xls(file):
    # start_time = time.time()

    excel_data_df = pd.read_excel(file)
    """ далее идет блок подготовки данных к анализу"""

    # Заменяем пробелы в названиях столбцов на знаки "_" и избавляемся от (.)
    excel_data_df = excel_data_df.rename(columns=lambda x: x.replace(' ', '_'))
    excel_data_df = excel_data_df.rename(columns=lambda x: x.replace('.', '_'))

    # переименуем столбец Исполнитель_МТО_(Ф_И_О) на Исполнитель_МТО ("отрежем" хвост _(Ф_И_О))
    excel_data_df = excel_data_df.rename(columns={'Исполнитель_МТО_(Ф_И_О_)': 'Исполнитель_МТО'})

    # заменим в числовых полях excel_data_df все отсутствующие данные (nan) на ноль (0)
    excel_data_df['Количество_ТМЦ'] = excel_data_df['Количество_ТМЦ'].fillna(0)
    excel_data_df['Кол-во_поставщика'] = excel_data_df['Кол-во_поставщика'].fillna(0)
    excel_data_df['Сумма_контракта'] = excel_data_df['Сумма_контракта'].fillna(0)

    # В основном датафрейме удалим все повторяющиеся строки в Лотах
    number_lots = del_nan(set(excel_data_df['Номер_лота']))
    for number_lot in number_lots:
        df_vrem = excel_data_df.loc[excel_data_df['Номер_лота'] == number_lot]
        if len(df_vrem) > 1:
            list_tup = []
            for ind in range(len(df_vrem)):
                ssl = df_vrem.iloc[[ind][0]].to_list()
                # ssl[4] = ssl[4].date()
                # ssl[5] = ssl[5].date()
                ssl = tuple(ssl)
                list_tup.append(ssl)
            c = Counter(list_tup)
            if set(c.values()) == {1}:
                continue
            else:
                list_unique_tup = set(list_tup)
                df_vrem = pd.DataFrame(list_unique_tup, columns=excel_data_df.columns)
                # удаляем из excel_data_df строки по номеру лота (number_lot)
                excel_data_df = excel_data_df[excel_data_df['Номер_лота'] != number_lot]
                excel_data_df = pd.concat([excel_data_df, df_vrem], ignore_index=True)
    # end_time = time.time()
    return excel_data_df

def upload_to_sql_df(df, conn, table):
    df.to_sql(table, conn, if_exists="replace", index=True)
    
def prep_basic_data():
    print('Мы сейчас здесь??')
