import threading
from tkinter import filedialog as fd
import pandas as pd
import time
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Notebook
from utils.logic import clean_data_from_xls, upload_to_sql_df, prep_basic_data
from utils.functions import del_nan
import sys

pd.options.display.float_format = '{:,.2f}'.format
import sqlite3


class SelectFrame:
    StringVar = ''

    def __init__(self, mywindow):
        self.data = {}
        self.progress = mywindow.progress_bar
        self.mywindow = mywindow
        self.frame = ttk.Frame(mywindow.notebook)
        self.mywindow.notebook.add(self.frame, text="Основные данные")
        data_df = self.mywindow.data_df
        self.columns_name = data_df.columns
        self.number_lots = del_nan(set(data_df['Номер_лота']))
        self.actor_names = del_nan(set(data_df['Исполнитель_МТО']))
        self.discipline_names = del_nan(set(data_df['Дисциплина']))
        self.project_names = del_nan(set(data_df['Наименование_проекта']))
        self.contragent_winners = del_nan(set(data_df['Присуждено_контрагенту']))
        self.currency_names = del_nan(set(data_df['Валюты_контракта']))
        self.set_frame_top()
        self.set_frame_middle()
        self.set_frame_bottom()
    
    def set_frame_top(self):
        # Основная статистика
        ...
        # frame_midd_right_top = Frame(self.frame)
        # frame_midd_right_top.pack(side=LEFT, fill=BOTH, expand=0)
        # frame_midd_right_bot = Frame(self.frame)
        # frame_midd_right_bot.pack(side=LEFT, fill=BOTH, expand=0)

        # label_midd_proj = Label(frame_midd_right_top, text="Количество проектов: ", height=0)
        # label_midd_proj.pack(side=TOP, expand=0, padx=10)
        # entry_midd_proj = Entry(self, width=20)
        # entry_midd_proj.pack(side=TOP,  expand=0, padx=10)
        # entry_midd_proj.insert(0, len(self.project_names))

        # label_midd_lot = Label(frame_midd_right_top, text="Количество лотов: ", height=0)
        # label_midd_lot.pack(side=TOP, expand=0, padx=10)
        # entry_midd_lot = Entry(frame_middle, width=20)
        # entry_midd_lot.pack(side=TOP, expand=0, padx=10)
        # entry_midd_lot.insert(0, len(self.number_lots))

        # label_midd_win = Label(frame_midd_right_top, text="Число победителей конкурсов ", height=0)
        # label_midd_win.pack(side=TOP, expand=0, padx=10)
        # entry_midd_win = Entry(frame_middle, width=20)
        # entry_midd_win.pack(side=TOP, expand=0, padx=10)
        # entry_midd_win.insert(0, len(self.contragent_winners))
        
    def set_frame_middle(self):
        # Названия таблиц
        frame_top = Frame(self.frame)
        frame_top.pack(side=TOP, expand=0, fill=X)

        Label(frame_top, text="Наименование столбцов", width=24, height=0).pack(side=LEFT, expand=0, padx=15)
        Label(frame_top, text="Номера лотов", width=15, height=2).pack(side=LEFT, expand=0, padx=1)
        Label(frame_top, text="ФИО исполнителей", width=20, height=2).pack(side=LEFT, expand=0, padx=4)
        Label(frame_top, text="Наименование дисциплин", width=30, height=2).pack(side=LEFT, padx=6)
        Label(frame_top, text="Наименование проектов", width=24, height=2).pack(side=LEFT, padx=6)
        Label(frame_top, text="Победители конкурсов", width=20, height=2).pack(side=LEFT, padx=6)
        Label(frame_top, text="Валюты контракта", width=20, height=2).pack(side=LEFT, padx=6)

    def set_frame_bottom(self):
        # Список данных для выбора
        frame_middle = Frame(self.frame, height=50)
        frame_middle.pack(side=TOP, fill=X, expand=0)

        # Вывод списка Наименований столбцов
        columns_var = StringVar(frame_middle, value=self.columns_name)
        list_box_1 = Listbox(frame_middle, listvariable=columns_var, width=24, height=15)
        list_box_1.pack(side=LEFT, fill=Y, expand=0, padx=5)
        list_box_1.yview_scroll(number=1, what="units")

        # Вывод списка Номера лотов
        number_lots_var = StringVar(frame_middle, value=self.number_lots)
        list_box_2 = Listbox(frame_middle, listvariable=number_lots_var, width=15, height=15)
        list_box_2.pack(side=LEFT, fill=Y, expand=0, padx=5)
        list_box_2.yview_scroll(number=1, what="units")

        # # Вывод списка Исполнителей_MTO
        actors_var = StringVar(frame_middle, value=sorted(self.actor_names))
        list_box_3 = Listbox(frame_middle, listvariable=actors_var, width=24, height=15)
        list_box_3.pack(side=LEFT, fill=Y, expand=0, padx=10)
        list_box_3.yview_scroll(number=1, what="units")

        # Вывод списка Дисциплин
        discipline_var = StringVar(frame_middle, value=sorted(self.discipline_names))
        list_box_4 = Listbox(frame_middle, listvariable=discipline_var, width=24, height=15)
        list_box_4.pack(side=LEFT, fill=Y, expand=0, padx=10)
        list_box_4.yview_scroll(number=1, what="units")

        # Вывод списка Наименование проекта
        project_names_var = StringVar(frame_middle, value=sorted(self.project_names))
        list_box_5 = Listbox(frame_middle, listvariable=project_names_var, width=24, height=15)
        list_box_5.pack(side=LEFT, fill=Y, expand=0, padx=10)
        list_box_5.yview_scroll(number=1, what="units")

        # # Вывод списка Победителей
        contragent_var = StringVar(frame_middle, value=sorted(self.contragent_winners))
        list_box_6 = Listbox(frame_middle, listvariable=contragent_var, width=24, height=15)
        list_box_6.pack(side=LEFT, fill=Y, expand=0, padx=5)
        list_box_6.yview_scroll(number=1, what="units")

        # # Вывод списка Валюты контракта
        currency_names_var = StringVar(frame_middle, value=self.currency_names)
        list_box_7 = Listbox(frame_middle, listvariable=currency_names_var, width=10, height=15)
        list_box_7.pack(side=LEFT, fill=Y, expand=0, padx=5)
        list_box_7.yview_scroll(number=1, what="units")