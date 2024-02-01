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
		start_time = time.time()
		conn = sqlite3.connect("data/sql_krd.db")
		data_df = pd.read_sql("select * from data_kp", conn)
		self.mywindow.data_df = data_df
		
		# data_df_grpd = data_df.groupby(['Номер_лота', 'Дата_закрытия_лота', 'Дисциплина', 'Исполнитель_МТО',
		#                                 'Присуждено_контрагенту', 'Валюты_контракта'])['Сумма_контракта'].sum()
		
		# Сгруппируем основной датафрейм
		ser_grouped = data_df.groupby(['Номер_лота', 'Дисциплина', 'Наименование_проекта', 'Дата_открытия_лота',
		                               'Дата_закрытия_лота', 'Исполнитель_МТО', 'Присуждено_контрагенту',
		                               'Валюты_контракта'])['Сумма_контракта'].sum()
		
		# Этот dict_base очень удобный и адекватный основной источник информации для
		# построения различного рода словарей
		dict_base = ser_grouped.to_dict()
		
		""" Построим на основе  dict_base несколько словарей """
		
		# 1. Построим словарь - dict_discip_actors (Дисциплины : Исполнители)
		
		# dict_discip_actors = {}
		# for disc_name in discipline_names:
		# 	disc_list = []
		# 	for key in dict_base:
		# 		if disc_name in key:
		# 			disc_list.append(key[5].partition(' (')[0])
		# 		else:
		# 			continue
		# 	disc_list = get_unique_only(disc_list)
		# 	disc_list = cut_list(disc_list)
		# 	dict_discip_actors[disc_name] = disc_list
		# dict_discip_actors - это словарь, где ключи - наименования Дисциплин,
		# значения - список Исполнителей (формат Фамилия Имя Отчество)
		
		# 2. Создаем второй словарь dict_act_contrg. Здесь придется работать с dict_base и
		# только что созданным dict_discip_actors
		
		# dict_act_contrg = {}
		# for key1, value in dict_discip_actors.items():
		# 	for val in value:
		# 		lst_tmp = []
		# 		for key in dict_base:
		# 			if key[5].partition(' (')[0] == val:
		# 				lst_tmp.append(key[6])
		# 			else:
		# 				continue
		# 		lst_tmp = get_unique_only(lst_tmp)
		# 		lst_tmp = cut_list(lst_tmp)
		# 		dict_act_contrg[val] = lst_tmp
		
		# frame2 = ttk.LabelFrame(self.notebook)
		# frame2.pack(anchor=NW, fill=BOTH)
		# self.notebook.add(frame2, text="Аналитика данных")
		
		# frame_bottom = Frame(frame1, height=5)
		# frame_bottom.pack(side=TOP, fill=X, expand=0)
		
		# label_bot = Label(frame_bottom, text="")
		# label_bot.pack(expand=1)
		
		# # Начинаем заполнение правой части окна frame_mddle
		# # Создадим LabelFrame в правой части frame_middle
		
		# Вызываем из нашего пакета utils модуля logic.py процедуру prep_basic_data
		# prep_basic_data(data_df)
		# print("Мы вернулись сюда же!!!")
		
		# perems = sys.argv
		# for perem in perems:
		#     print(perem)
		
		# label_bot1 = Label(frame_bottom, text="Все лоты в интервале: ", height=0)
		# label_bot1.pack(side=LEFT, expand=0)
		
		# # Создаем поле Entry и в него записываем диапазон дат завершения лотов
		# entry = Entry(frame_bottom)
		# entry.pack(side=LEFT, expand=0)
		# my_variable = perems[0] + ' - ' + perems[1]
		# entry.insert(0, my_variable)
		
		# Группировка data_df - суммы и средние значения сумм в разрезе валют
		# по дисциплинам Компании
		# agg_sum = {'Сумма_контракта': ['sum', 'mean']}
		# data_df.groupby(['Дисциплина', 'Валюты_контракта']).agg(agg_sum)
		#
		# # Суммы контрактов (проработок) по проектам Компании в разрезе валют
		# agg_sum = {'Сумма_контракта': ['sum', 'mean']}
		# data_df.groupby(['Наименование_проекта', 'Валюты_контракта']).agg(agg_sum)
		#
		# # Количество контрактов (проработок) в разрезе Дисциплин
		# agg_func_count = {'Дисциплина': ['count']}
		# print(data_df.groupby(['Дисциплина', 'Валюты_контракта']).agg(agg_func_count))
		#
		# # а как это количество проработок делится между Исполителями?
		# agg_func_count = {'Дисциплина': ['count']}
		# data_actors_count = data_df.groupby(['Дисциплина', 'Исполнитель_МТО', 'Валюты_контракта']).agg(agg_func_count)
		# print(data_actors_count)
		#
		# # Группировка data_df - суммы и средние значения сумм в разрезе валют
		# # по дисциплинам Компании
		# agg_sum = {'Сумма_контракта': ['sum', 'mean']}
		# print(data_df.groupby(['Дисциплина', 'Валюты_контракта']).agg(agg_sum))
		#
		# # Суммы контрактов (прработок) по проектам Компании в разрезе валют
		# agg_sum = {'Сумма_контракта': ['sum', 'mean']}
		# print(data_df.groupby(['Наименование_проекта', 'Валюты_контракта']).agg(agg_sum))
		#
		# # Количество контрактов (проработок) в разрезе Дисциплин
		# agg_func_count = {'Дисциплина': ['count']}
		# print(data_df.groupby(['Дисциплина', 'Валюты_контракта']).agg(agg_func_count))
		#
		# # а как это количество проработок делится между Исполителями?
		# agg_func_count = {'Дисциплина': ['count']}
		# data_actors_count = data_df.groupby(['Дисциплина', 'Исполнитель_МТО', 'Валюты_контракта']).agg(agg_func_count)
		# print(data_actors_count)
