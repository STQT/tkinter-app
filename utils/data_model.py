import threading
from tkinter import filedialog as fd
import pandas as pd
import time
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Notebook
from utils.logic import clean_data_from_xls, upload_to_sql_df, prep_basic_data
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
        self.notebook = ttk.Notebook()
        self.notebook.pack(expand=True, fill=BOTH)
        # Создадим фреймы
        frame1 = ttk.LabelFrame(self.notebook, height=5)
        # frame1.pack(anchor=NW, fill=BOTH)
        
        frame_top = Frame(frame1, height=5)
        frame_top.pack(anchor=NW, fill=X)
        
        Label(frame_top, text="Наименование столбцов", width=20, height=2).pack(side=LEFT, padx=2)
        Label(frame_top, text="Номера лотов", width=20, height=2).pack(side=LEFT, padx=1)
        Label(frame_top, text="ФИО исполнителей", width=20, height=2).pack(side=LEFT, padx=2)
        Label(frame_top, text="Наименование дисциплин", width=20, height=2).pack(side=LEFT, padx=6)
        Label(frame_top, text="Наименование проектов", width=20, height=2).pack(side=LEFT, padx=6)
        Label(frame_top, text="Победители конкурсов", width=20, height=2).pack(side=LEFT, padx=6)
        Label(frame_top, text="Валюты контракта", width=20, height=2).pack(side=LEFT, padx=6)
        
        frame_middle = Frame(frame1, height=40)
        frame_middle.pack(anchor=CENTER, fill=Y)
        
        frame2 = ttk.LabelFrame(self.notebook)
        frame2.pack(anchor=NW, fill=BOTH)
        
        # Добавим фреймы в качестве вкладок
        self.notebook.add(frame1, text="Основные данные")
        self.notebook.pack(anchor=NW, side=TOP, fill=Y)
        self.notebook.add(frame2, text="Аналитика данных")
        self.notebook.pack()

        # Вывод списка Наименований столбцов
        columns_var = StringVar(frame_middle, value=columns_name)
        list_box_1 = Listbox(frame_middle, listvariable=columns_var, width=24)
        list_box_1.pack(side=LEFT, fill=BOTH, expand=0, padx=5)
        list_box_1.yview_scroll(number=1, what="units")

        # Вывод списка Номера лотов
        number_lots_var = StringVar(frame_middle, value=number_lots)
        list_box_2 = Listbox(frame_middle, listvariable=number_lots_var, width=15)
        list_box_2.pack(side=LEFT, fill=BOTH, expand=0, padx=5, ipadx=5, ipady=5)
        list_box_2.yview_scroll(number=1, what="units")

        # # Вывод списка Исполнителей_MTO
        actors_var = StringVar(frame_middle, value=sorted(actor_names))
        list_box_3 = Listbox(frame_middle, listvariable=actors_var, width=24)
        list_box_3.pack(side=LEFT, fill=BOTH, expand=0, padx=5, ipadx=5, ipady=5)
        list_box_3.yview_scroll(number=1, what="units")

        # Вывод списка Дисциплин
        discipline_var = StringVar(frame_middle, value=sorted(discipline_names))
        list_box_4 = Listbox(frame_middle, listvariable=discipline_var, width=24)
        list_box_4.pack(side=LEFT, fill=BOTH, expand=0, padx=5, ipadx=5, ipady=5)
        list_box_4.yview_scroll(number=1, what="units")

        # # Вывод списка Наименований проектов
        projects_var = StringVar(frame_middle, value=sorted(project_names))
        list_box_5 = Listbox(frame_middle, listvariable=projects_var, width=24)
        list_box_5.pack(side=LEFT, fill=BOTH, expand=0, padx=5, ipadx=5, ipady=5)
        list_box_5.yview_scroll(number=1, what="units")

        # # Вывод списка Победителей
        contragent_var = StringVar(frame_middle, value=sorted(contragent_winners))
        list_box_6 = Listbox(frame_middle, width=24, listvariable=contragent_var)
        list_box_6.pack(side=LEFT, fill=BOTH, expand=0, padx=5, ipadx=5, ipady=5)
        list_box_6.yview_scroll(number=1, what="units")

        # # Вывод списка Валюты контракта
        currency_names_var = StringVar(frame_middle, value=currency_names)
        list_box_7 = Listbox(frame_middle, listvariable=currency_names_var, width=10)
        list_box_7.pack(side=LEFT, fill=BOTH, expand=0, padx=5, ipadx=5, ipady=5)
        list_box_7.yview_scroll(number=1, what="units")
        
        frame_bottom = Frame(frame1, height=5)
        frame_bottom.pack()

        label_bot = Label(frame_bottom, text="Наполняем фрейм расчетными основными данными.")
        label_bot.pack(expand=1)
        