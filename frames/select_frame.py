import threading
from tkinter import filedialog as fd
import pandas as pd
import time
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Notebook
from utils.functions import del_nan
from utils.logic import prep_basic_data, prepare_main_datas
# from utils.functions import OpenListbox
from frames import search_in_Listbox
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
		print('Пошагово выполнили все инструкции!!')
	
	def set_frame_top(self):
		# Основная статистика
		frame_top = Frame(self.frame, height=100, bg='blue', bd=1, relief='raised')
		frame_top.pack(side=TOP, fill=X, expand=0)
		""" для вычисления beg_end_date вызываем prep_basic_data(self.mywindow.data_df)"""
		beg_end_date = prep_basic_data(self.mywindow.data_df)
		print(beg_end_date)
		our_range = beg_end_date[0] + ' - ' + beg_end_date[1]
		""" за получением этого результата мы обращаемся в модуль prepare_main_datas(self.mywindow.data_df) """
		# disc_sum = prepare_main_datas(self.mywindow.data_df)
		# print(disc_sum)
		# r_actors_count = prepare_main_datas(self.mywindow.data_df)
		#print(r_actors_count)
		
		# заполняем первый фрейм Основных данных
		frame_ontop_1 = Frame(frame_top, height=5, bd=1, relief='raised', padx=5, pady=5)
		frame_ontop_1.pack(side=TOP, expand=0, fill=X)
		
		label_ontop_1_date = Label(frame_ontop_1, text="Данные из базы в интервале: ", height=0)
		label_ontop_1_date.pack(side=LEFT, expand=0, padx=10)
		entry_top_proj = Entry(frame_ontop_1, width=26)
		entry_top_proj.pack(side=LEFT, expand=0)
		entry_top_proj.insert(0, our_range)
		
		label_ontop_proj = Label(frame_ontop_1, text="Количество проектов: ", height=0)
		label_ontop_proj.pack(side=LEFT, expand=0, padx=10)
		entry_top_proj = Entry(frame_ontop_1, width=8)
		entry_top_proj.pack(side=LEFT, expand=0)
		entry_top_proj.insert(0, len(self.project_names))
		
		label_ontop_1_lot = Label(frame_ontop_1, text="Количество лотов: ", height=0)
		label_ontop_1_lot.pack(side=LEFT, expand=0, padx=10)
		entry_top_lot = Entry(frame_ontop_1, width=8)
		entry_top_lot.pack(side=LEFT, expand=0)
		entry_top_lot.insert(0, len(self.number_lots))
		
		label_ontop_1_win = Label(frame_ontop_1, text="Число победителей конкурсов ", height=0)
		label_ontop_1_win.pack(side=LEFT, expand=0, padx=10)
		entry_top_win = Entry(frame_ontop_1, width=8)
		entry_top_win.pack(side=LEFT, expand=0, padx=10)
		entry_top_win.insert(0, len(self.contragent_winners))
		
		frame_ontop_2 = Frame(frame_top, height=5, bg='yellow', bd=1, relief='raised', padx=5, pady=5)
		frame_ontop_2.pack(side=TOP, expand=0, fill=X)
		Label(frame_ontop_2, text='We are here').pack(side=LEFT, expand=0, padx=5)
		
		frame_ontop_3 = Frame(frame_top, height=5, bg='blue', bd=1, relief='raised', padx=5, pady=5)
		frame_ontop_3.pack(anchor=NW, expand=0, fill=X)
		Label(frame_ontop_3, text='Сейчас мы здесь').pack(side=LEFT, expand=0, padx=5)
		
		frame_ontop_4 = Frame(frame_top, height=5, bg='brown', bd=1, relief='raised', padx=5, pady=5)
		frame_ontop_4.pack(side=TOP, expand=0, fill=X)
		Label(frame_ontop_4, text='We are here').pack(side=LEFT, expand=0, padx=5)
		
		frame_ontop_5 = Frame(frame_top, height=5, bg='yellow', bd=1, relief='raised', padx=5, pady=5)
		frame_ontop_5.pack(side=TOP, expand=0, fill=X)
		Label(frame_ontop_5, text='We are here').pack(side=LEFT, expand=0, padx=5)
	
	def set_frame_middle(self):
		# Названия таблиц
		frame_middle = Frame(self.frame, height=100, bd=1, relief='raised')
		frame_middle.pack(side=TOP, expand=0, fill=X, padx=5, pady=5)
		
		frame_midd_1 = Frame(frame_middle)
		frame_midd_1.pack(side=TOP, expand=0, fill=X)
		Label(frame_midd_1, text="Cтолбцы таблицы БД", height=0).pack(side=LEFT, expand=0, padx=5)
		Label(frame_midd_1, text="Номера лотов", height=2).pack(side=LEFT, expand=0, padx=5)
		Label(frame_midd_1, text="ФИО исполнителей", height=2).pack(side=LEFT, expand=0, padx=5)
		Label(frame_midd_1, text="Наименование дисциплин", height=2).pack(side=LEFT, expand=0, padx=5)
		Label(frame_midd_1, text="Наименование проектов", height=2).pack(side=LEFT, expand=0, padx=5)
		Label(frame_midd_1, text="Победители конкурсов", height=2).pack(side=LEFT, expand=0, padx=5)
		Label(frame_midd_1, text="Валюты контракта", height=2).pack(side=LEFT, expand=0, padx=5)
		
		frame_midd_2 = Frame(frame_middle, height=25, bd=1, relief='raised')
		frame_midd_2.pack(side=TOP, expand=0, fill=X)
		
		# Вывод списка Наименований столбцов
		columns_var = StringVar(frame_midd_2, value=self.columns_name)
		list_box_1 = Listbox(frame_midd_2, listvariable=columns_var, width=20, height=20)
		list_box_1.pack(side=LEFT, fill=Y, expand=0, padx=5)
		list_box_1.yview_scroll(number=1, what="units")
		
		# Вывод списка Номера лотов
		number_lots_var = StringVar(frame_midd_2, value=self.number_lots)
		list_box_2 = Listbox(frame_midd_2, listvariable=number_lots_var, width=12, height=20)
		list_box_2.pack(side=LEFT, fill=Y, expand=0, padx=5)
		list_box_2.yview_scroll(number=1, what="units")
		
		# # Вывод списка Исполнителей_MTO
		# master = frame_midd_2
		# print('Сейчас перейдем в модуль functions')
		# self.widget_container = OpenListbox(master, self.actor_names)
		actors_var = StringVar(frame_midd_2, value=sorted(self.actor_names))
		list_box_3 = Listbox(frame_midd_2, listvariable=actors_var, width=18, height=15)
		list_box_3.pack(side=LEFT, fill=Y, expand=0, padx=15)
		list_box_3.yview_scroll(number=1, what="units")
		# Вывод списка Дисциплин
		discipline_names_var = StringVar(frame_midd_2, value=sorted(self.discipline_names))
		list_box_4 = Listbox(frame_midd_2, listvariable=discipline_names_var, width=22, height=15)
		list_box_4.pack(side=LEFT, fill=Y, expand=0, padx=10)
		list_box_4.yview_scroll(number=1, what="units")
		
		# # Вывод списка Наименований проектов
		project_names_var = StringVar(frame_midd_2, value=sorted(self.project_names))
		list_box_5 = Listbox(frame_midd_2, listvariable=project_names_var, width=21, height=15)
		list_box_5.pack(side=LEFT, fill=Y, expand=0, padx=10)
		list_box_5.yview_scroll(number=1, what="units")
		
		# # Вывод списка Победителей конкурса
		contragent_winners_var = StringVar(frame_midd_2, value=sorted(self.contragent_winners))
		list_box_6 = Listbox(frame_midd_2, listvariable=contragent_winners_var, width=22, height=15)
		list_box_6.pack(side=LEFT, fill=Y, expand=0, padx=10)
		list_box_6.yview_scroll(number=1, what="units")
		
		# # Вывод списка Валюты контракта
		currency_names_var = StringVar(frame_midd_2, value=sorted(self.currency_names))
		list_box_6 = Listbox(frame_midd_2, listvariable=currency_names_var, width=18, height=15)
		list_box_6.pack(side=LEFT, fill=Y, expand=0, padx=10)
		list_box_6.yview_scroll(number=1, what="units")
	
	def set_frame_bottom(self):
		...
# frame_midd_right_bot = Frame(self.frame)
# frame_midd_right_bot.pack(side=LEFT, fill=BOTH, expand=0)
# # Список данных для выбора
#
#
# # Вывод списка Дисциплин
# discipline_var = StringVar(frame_middle, value=sorted(self.discipline_names))
# list_box_4 = Listbox(frame_middle, listvariable=discipline_var, width=24, height=15)
# list_box_4.pack(side=LEFT, fill=Y, expand=0, padx=10)
# list_box_4.yview_scroll(number=1, what="units")
#
# # Вывод списка Наименование проекта
# project_names_var = StringVar(frame_middle, value=sorted(self.project_names))
# list_box_5 = Listbox(frame_middle, listvariable=project_names_var, width=24, height=15)
# list_box_5.pack(side=LEFT, fill=Y, expand=0, padx=10)
# list_box_5.yview_scroll(number=1, what="units")
#
# # # Вывод списка Победителей
# contragent_var = StringVar(frame_middle, value=sorted(self.contragent_winners))
# list_box_6 = Listbox(frame_middle, listvariable=contragent_var, width=24, height=15)
# list_box_6.pack(side=LEFT, fill=Y, expand=0, padx=5)
# list_box_6.yview_scroll(number=1, what="units")
#
# # # Вывод списка Валюты контракта
# currency_names_var = StringVar(frame_middle, value=self.currency_names)
# list_box_7 = Listbox(frame_middle, listvariable=currency_names_var, width=10, height=15)
# list_box_7.pack(side=LEFT, fill=Y, expand=0, padx=5)
# list_box_7.yview_scroll(number=1, what="units")
