from tkinter import filedialog as fd
import itertools
from itertools import groupby
import operator
from operator import itemgetter
import pandas as pd
import numpy as np
from datetime import date as dt
from collections import Counter
import time

pd.options.display.float_format = '{:,.2f}'.format
import sqlite3


def del_nan(list_name):
	L1 = [item for item in list_name if not (pd.isnull(item)) is True]
	L1, list_name = list_name, L1
	return list_name


class DataModel:
	def __init__(self):
		self.data = {}
	
	def set_data(self, key, value):
		self.data[key] = value
	
	def get_data(self, key):
		return self.data.get(key, None)
	
	def open_file(self):
		wanted_files = (('Data files', '*.xlsx; *.csv'),
		                ('All', '*.*'))
		file_name = fd.askopenfilename(initialdir="D:/", title="Find a File",
		                               filetypes=wanted_files)
		
		start_time = time.time()

		excel_data_df = pd.read_excel(file_name)
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
			df_vrem = ''
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
		
		end_time = time.time()
		action_time = end_time - start_time
		print('Время загрузки файла Excel =', action_time, '(милли/микро) секунд')
		
		""" Здесь все подготовленные данные записываем в Базу Данных SQL"""
		# db_path = "D:\PythonProjects\sql_krd.db"
		conn = sqlite3.connect("D:\PythonProjects\sql_krd.db")
		excel_data_df.to_sql("data_kp", conn, if_exists="replace", index=True)
	
	def open_from_db(self):
		start_time = time.time()
		conn = sqlite3.connect("D:\PythonProjects\sql_krd.db")
		data_df = pd.read_sql("select * from data_kp", conn)
		
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
