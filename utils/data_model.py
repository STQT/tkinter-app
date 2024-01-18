import threading
from tkinter import filedialog as fd
import pandas as pd
import time

from utils.logic import clean_data_from_xls, upload_to_sql_df
from utils.functions import del_nan

pd.options.display.float_format = '{:,.2f}'.format
import sqlite3


class DataModel:
    def __init__(self, mywindow):
        self.data = {}
        self.progress = mywindow.progress_bar
        self.window = mywindow

    def set_data(self, key, value):
        self.data[key] = value

    def get_data(self, key):
        return self.data.get(key, None)

    def open_file(self):
        wanted_files = (('Data files', '*.xlsx;*.csv'),
                        ('All', '*.*'))
        file_name = fd.askopenfilename(initialdir="D:/", title="Find a File",
                                       filetypes=wanted_files)

        def real_traitement():
            self.progress.start()
            df = clean_data_from_xls(file_name)
            conn = sqlite3.connect("data/sql_krd.db")
            upload_to_sql_df(df, conn, "data_kp")
            self.progress.stop()

        threading.Thread(target=real_traitement).start()

    def open_from_db(self):
        self.window.label_isp.config(text='Kairat')
        start_time = time.time()
        conn = sqlite3.connect("data/sql_krd.db")
        data_df = pd.read_sql("select * from data_kp", conn)
        print(type(data_df))

        columns_name = data_df.columns
        print(columns_name)
        # уникальные номера Лотов
        number_lots = del_nan(set(data_df['Номер_лота']))
        print(number_lots)
        # ФИО исполнителей Лотов (закупщиков)
        actor_names = del_nan(set(data_df['Исполнитель_МТО']))
        print(actor_names)
        # Наименования дисциплин
        discipline_names = del_nan(set(data_df['Дисциплина']))
        print(discipline_names)
        # Наименование проектов Компании
        project_names = del_nan(set(data_df['Наименование_проекта']))
        print(project_names)
        # Контрагенты - победители Лотов
        contragent_winners = del_nan(set(data_df['Присуждено_контрагенту']))
        print(contragent_winners)
        # Валюты контрактов
        currency_names = del_nan(set(data_df['Валюты_контракта']))
        print(currency_names)

        data_df_grpd = data_df.groupby(['Номер_лота', 'Дисциплина', 'Исполнитель_МТО',
                                        'Присуждено_контрагенту', 'Валюты_контракта'])['Сумма_контракта'].sum()
        print(data_df_grpd)

        end_time = time.time()
        action_time = end_time - start_time
        print('Время загрузки из БД и вычисления =', action_time, '(милли/микро) секунд')
