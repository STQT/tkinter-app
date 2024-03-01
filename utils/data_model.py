""" Достойный материал-туториал - https://habr.com/ru/articles/321510/ ( ниже по коду )"""
import os
import threading
from tkinter import filedialog as fd
import pandas as pd
import time
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Notebook
from utils.logic import clean_data_from_xls, upload_to_sql_df, clean_contr_data_from_xls

from utils.functions import del_nan, get_unique_only, cut_list
import sys

pd.options.display.float_format = '{:,.2f}'.format
import sqlite3


class DataModel:
    StringVar = ''
    def __init__(self, mywindow):
        self.data = {}
        self.progress = mywindow.progress_bar
        self.mywindow = mywindow

    def set_data(self, key, value):
        self.data[key] = value

    def get_data(self, key):
        return self.data.get(key, None)

    def open_file(self):
        wanted_files = (('Data files', '*.xlsx;*.csv'),
                        ('All', '*.*'))
        file_path = fd.askopenfilename(initialdir="D:/", title="Find a File",
                                       filetypes=wanted_files)

        def real_traitement():
            self.progress.start()
            file_name = os.path.basename(file_path)
            name, extension = file_name.rsplit(".", 1)
            simb = name.split("_", 1)[0]
            if simb == 'KP':
                df = clean_data_from_xls(file_path)
                conn = sqlite3.connect("data/sql_krd.db")
                cur = conn.cursor()
                cur.execute("DELETE FROM data_tmp")
                upload_to_sql_df(df, conn, "data_tmp")
                cur.executescript(
                    """insert into data_kp(lot_number, lot_status, discipline, project_name,
                        open_date, close_date, actor_name, good_name,
                        good_count, unit, supplier_qty, supplier_unit,
                        winner_name, unit_price, total_price, currency)
                    select
                    a.lot_number, a.lot_status, a.discipline, a.project_name,
                    a.open_date, a.close_date, a.actor_name, a.good_name,
                    a.good_count, a.unit, a.supplier_qty, a.supplier_unit,
                    a.winner_name, a.unit_price, a.total_price, a.currency
                    from data_tmp as a;"""
                )
            else:
                df = clean_contr_data_from_xls(file_path)
                conn = sqlite3.connect("data/sql_krd.db")
                # upload_to_sql_df(df, conn, "data_contr_tmp")
                df.to_sql("data_contr_tmp", conn, if_exists="append", index=True)
                cur = conn.cursor()
                cur.executescript(
                    '''UPDATE data_contr_tmp SET close_date = substr(close_date, 7, 4)
								|| '-' || substr(close_date, 4, 2) || '-' || substr(close_date, 1, 2);
				UPDATE data_contr_tmp SET contract_date = substr(contract_date, 7, 4)
				|| '-' || substr(contract_date, 4, 2) || '-' || substr(contract_date, 1, 2);''')
            
            
            self.progress.stop()

        threading.Thread(target=real_traitement).start()


    def open_from_db(self):
        start_time = time.time()
        conn = sqlite3.connect("data/sql_krd.db")
        data_df = pd.read_sql("select * from data_kp", conn)
        self.mywindow.data_df = data_df

        print('Возвращаемся в место вызова')

    def prepare_dicts(self):
        print('Теперь мы здесь')
        self.discipline_names = del_nan(set(self.mywindow.data_df['Дисциплина']))

        vib_contr_acts = pd.crosstab(self.mywindow.data_df['Присуждено_контрагенту'],
                                     [self.mywindow.data_df['Исполнитель_МТО']])

        list_acts = vib_contr_acts.columns
        list_acts = cut_list(list_acts)
        vib_actors = vib_contr_acts.rename(columns=dict(zip(vib_contr_acts.columns, list_acts)))

        # сгруппируем основной датафрейм
        df_grouped = \
            self.mywindow.data_df.groupby(['Номер_лота', 'Дисциплина', 'Наименование_проекта', 'Дата_открытия_лота',
                                           'Дата_закрытия_лота', 'Исполнитель_МТО', 'Присуждено_контрагенту',
                                           'Валюты_контракта'])['Сумма_контракта'].sum()
        dict_base = df_grouped.to_dict()

        # Построим на основе  dict_base несколько словарей
        #  Построим словарь - dict_discip_actors (Дисциплины : Исполнители)

        dict_discip_actors = {}
        for disc_name in self.discipline_names:
            disc_list = []
            for key in dict_base:
                if disc_name in key:
                    disc_list.append(key[5].partition(' (')[0])
                    continue
                else:
                    continue
            disc_list = get_unique_only(disc_list)
            disc_list = cut_list(disc_list)
            dict_discip_actors[disc_name] = disc_list

            # print(dict_discip_actors)

        # dict_discip_actors - это словарь, где ключи - наименования Дисциплин,
        # значения - список Исполнителей (формат Фамилия Имя Отчество)

        #  Создаем второй словарь dict_act_contrg. Здесь придется работать с dict_base и
        # только что созданным dict_discip_actors

        dict_act_contrg = {}
        for key1, value in dict_discip_actors.items():
            for val in value:
                lst_tmp = []
                for key in dict_base:
                    if key[5].partition(' (')[0] == val:
                        lst_tmp.append(key[6])
                    else:
                        continue
                lst_tmp = get_unique_only(lst_tmp)
                lst_tmp = cut_list(lst_tmp)
                dict_act_contrg[val] = lst_tmp

        # еще один словарь - {дисциплина: {исполнитель : (Контрагент , частота заключ. контрактов)}}
        dict_disc_act_freq = {}
        for key, value in dict_discip_actors.items():
            list_key = []
            dict_var_tmp = {}
            for val in value:
                tupl_list = []
                i = 0
                for idx in vib_actors.index:
                    if vib_actors.loc[idx, val] != 0:
                        tupl_tmp = (idx, vib_actors.loc[idx, val])
                        tupl_list.append(tupl_tmp)
                    i = i + 1
                tupl_list.sort(key=lambda x: x[1], reverse=True)
                dict_var_tmp[val] = tupl_list
            list_key.append(dict_var_tmp)
            dict_disc_act_freq[key] = list_key
        print('Мы завершили создание словарей!')
        # print(dict_disc_act_freq.values())
