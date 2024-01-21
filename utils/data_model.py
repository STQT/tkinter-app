import threading
from tkinter import filedialog as fd
import pandas as pd
import time
from tkinter import *
from tkinter import ttk

from utils.logic import clean_data_from_xls, upload_to_sql_df
from utils.functions import del_nan

pd.options.display.float_format = '{:,.2f}'.format
import sqlite3


class DataModel:
    StringVar = ''

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
        # self.window.label_isp.config(text='Kairat')

        start_time = time.time()
        conn = sqlite3.connect("data/sql_krd.db")
        data_df = pd.read_sql("select * from data_kp", conn)

        columns_name = data_df.columns
        number_lots = del_nan(set(data_df['Номер_лота']))
        actor_names = del_nan(set(data_df['Исполнитель_МТО']))
        discipline_names = del_nan(set(data_df['Дисциплина']))
        project_names = del_nan(set(data_df['Наименование_проекта']))
        contragent_winners = del_nan(set(data_df['Присуждено_контрагенту']))
        currency_names = del_nan(set(data_df['Валюты_контракта']))

        # data_df_grpd = data_df.groupby(['Номер_лота', 'Дисциплина', 'Исполнитель_МТО',
        #                                 'Присуждено_контрагенту', 'Валюты_контракта'])['Сумма_контракта'].sum()

        # label_isp = Label(text="Основные данные для анализа")
        # label_isp.pack(anchor=N, side=LEFT, expand=1)

        # Создадим набор вкладок
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(self.window, expand=True, fill=BOTH)
        # Создадим фреймы
        frame1 = ttk.LabelFrame(self.notebook, text="Main Window")
        frame1.pack(self.notebook, fill=BOTH, expand=True)
        frame2 = ttk.LabelFrame(self.notebook)
        frame2.pack(fill=BOTH, expand=True)
        # Добавим фреймы в качестве вкладок
        self.notebook.add(frame1, text="Основные данные")
        self.notebook.pack()
        self.notebook.add(frame2, text="Аналитика данных")
        self.notebook.pack()

        label_frm1 = Label(frame1, text="Основные данные")
        label_frm1.pack()

        columns_var = StringVar(value=columns_name)
        list_box_1 = Listbox(listvariable=columns_var, width=35)
        list_box_1.pack(anchor=NW, side=LEFT, fill=Y, expand=1, padx=5, pady=5, ipadx=5, ipady=5)
        list_box_1.yview_scroll(number=1, what="units")

        contragent_var = StringVar(value=sorted(contragent_winners))
        list_box_6 = Listbox(listvariable=contragent_var, width=45)
        list_box_6.pack(anchor=W, side=LEFT, fill=Y, expand=1, padx=5, pady=5, ipadx=5, ipady=5)
        list_box_6.yview_scroll(number=1, what="units")
