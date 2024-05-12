import threading
from tkinter import filedialog as fd
import pandas as pd
import time
from tkinter import *
from tkinter import ttk
from utils.functions import del_nan, calc_indicators, prepare_main_datas
from utils.functions import create_treeview_table, scroll_box, param_query
from utils.logic import connect_to_database
# from utils.functions import OpenListbox
from frames import search_in_Listbox
import sys
import sqlite3

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
		
		# соединяемся с базой данных через функцию open_dbase
		query = "SELECT DISTINCT(lot_number) FROM data_kp;"
		self.number_lots = calc_indicators(query)
		
		query = "select DISTINCT(actor_name) from data_kp order by actor_name"
		self.actor_names = calc_indicators(query)
		
		query = "select DISTINCT(discipline) from data_kp order by discipline"
		self.discipline_names = calc_indicators(query)
		
		query = "select DISTINCT(project_name) from data_kp order by project_name"
		self.project_names = calc_indicators(query)
		
		query = "select DISTINCT(winner_name) from data_kp order by winner_name"
		self.contragent_winners = calc_indicators(query)
		
		query = "select DISTINCT(currency) from data_kp where currency not null order by currency"
		self.currency_names = calc_indicators(query)
		
		self.set_frame_top()
		self.set_frame_middle()
		self.set_frame_bottom()
		print('Пошагово выполнили все инструкции!!')
	
	def set_frame_top(self):
		# Основная статистика
		frame_top = ttk.Frame(self.frame, height=100, relief='raised')
		frame_top.pack(side=TOP, fill=BOTH, expand=0)
		frame_top.config()
		""" для вычисления beg_end_date вызываем prep_basic_data(self.mywindow.data_df)"""
		# beg_end_date = connect_to_database(self.mywindow.data_df) - потом Удалить
		# создадим переменную с именем базы данных
		db_name = 'data/sql_krd_new.db'
		beg_end_date = connect_to_database(db_name)
		print(beg_end_date)
		
		# заполняем первый фрейм Основных данных
		frame_ontop_1 = Frame(frame_top, height=5, bd=1, relief='raised',
		                      padx=5, pady=5)
		frame_ontop_1.pack(side=TOP, expand=0, fill=X)
		
		label_ontop_1_date = Label(frame_ontop_1, text="Данные из базы в интервале: ",
		                           height=0)
		label_ontop_1_date.pack(side=LEFT, expand=0, padx=10)
		entry_top_proj = Entry(frame_ontop_1, width=26)
		entry_top_proj.pack(side=LEFT, expand=0)
		entry_top_proj.insert(0, beg_end_date)
		
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
		
		frame_ontop_2 = Frame(frame_top, height=5, bg='#d7d8e0', bd=1, relief='raised', padx=5, pady=5)
		frame_ontop_2.pack(side=LEFT, fill=BOTH, expand=1)
		
		
		# -------------------------------------------------
		# здесь пример параметризации запросов к базе SQLite
		table_name = "data_kp"

		values = ['М5-ЭКСПОРТ ООО', 'Бойсун ГПЗ (ЕРС)', '2023-01-01']
		
		conn = sqlite3.connect("data\sql_krd.db")
		cur = conn.cursor()
		cur.execute("SELECT count(distinct lot_number) "
		            "FROM data_kp WHERE (winner_name = ?) "
		            "AND (project_name = ?) AND (close_date >= ?)",
		            (tuple(values))) # список конвертирован в кортеж. И это основное требование SQLite
		print('Что мы должны получить??')
		print(cur.fetchall())
		conn.close()
		# ------------------------------------------------
		
		
		frame_ontop_3 = Frame(frame_top, height=5, bg='#c0c0c0', bd=1, relief='raised', padx=5, pady=5)
		frame_ontop_3.pack(anchor=NW, expand=0, fill=X)
		Label(frame_ontop_3, text='Сейчас мы здесь').pack(side=LEFT, expand=0, padx=5)
		
		frame_ontop_4 = Frame(frame_top, height=5, bg='#d8dfd8', bd=1, relief='raised', padx=5, pady=5)
		frame_ontop_4.pack(side=TOP, expand=0, fill=X)
		Label(frame_ontop_4, text='We are here').pack(side=LEFT, expand=0, padx=5)
		
		frame_ontop_5 = Frame(frame_top, height=5, bg='#00008b', bd=1, relief='raised', padx=5, pady=5)
		frame_ontop_5.pack(side=TOP, expand=0, fill=X)
		Label(frame_ontop_5, text='We are here').pack(side=LEFT, expand=0, padx=5)
	
	def set_frame_middle(self):
		# Названия таблиц
		frame_middle = Frame(self.frame, height=100, bd=1, relief='raised')
		frame_middle.pack(side=TOP, expand=0, fill=BOTH, padx=5, pady=5)
		
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
		number_lots_var = StringVar(frame_midd_2, value=sorted(self.number_lots))
		list_box_2 = Listbox(frame_midd_2, listvariable=number_lots_var, width=12, height=20)
		list_box_2.pack(side=LEFT, fill=Y, expand=0, padx=5)
		list_box_2.yview_scroll(number=1, what="units")
		
		# # Вывод списка Исполнителей_MTO
		actors_var = StringVar(frame_midd_2, self.actor_names)
		list_box_3 = Listbox(frame_midd_2, listvariable=actors_var, width=18, height=15)
		list_box_3.pack(side=LEFT, fill=Y, expand=0, padx=15)
		list_box_3.yview_scroll(number=1, what="units")
		# добавим scrollbox
		
		scroll_param1 = list_box_3
		scroll_param2 = frame_midd_2
		scroll_box(scroll_param1, scroll_param2)
		# scrollbar = ttk.Scrollbar(scroll_param2, orient=VERTICAL, command=scroll_param1.yview)
		# scrollbar.pack(side=RIGHT, fill=Y, anchor=E)
		# scroll_param1["yscrollcommand"] = scrollbar.set
		
		# Вывод списка Дисциплин
		discipline_names_var = StringVar(frame_midd_2, value=self.discipline_names)
		list_box_4 = Listbox(frame_midd_2, listvariable=discipline_names_var, width=22, height=15)
		list_box_4.pack(side=LEFT, fill=Y, expand=0, padx=10)
		list_box_4.yview_scroll(number=1, what="units")
		
		# # Вывод списка Наименований проектов
		project_names_var = StringVar(frame_midd_2, value=self.project_names)
		list_box_5 = Listbox(frame_midd_2, listvariable=project_names_var, width=21, height=15)
		list_box_5.pack(side=LEFT, fill=Y, expand=0, padx=10)
		list_box_5.yview_scroll(number=1, what="units")
		
		# # Вывод списка Победителей конкурса
		contragent_winners_var = StringVar(frame_midd_2, self.contragent_winners)
		list_box_6 = Listbox(frame_midd_2, listvariable=contragent_winners_var, width=22, height=15)
		list_box_6.pack(side=LEFT, fill=Y, expand=0, padx=10)
		list_box_6.yview_scroll(number=1, what="units")
		# добавим scrollbox
		scroll_param1 = list_box_6
		scroll_param2 = frame_midd_2
		scroll_box(scroll_param1, scroll_param2)
		
		# # Вывод списка Валюты контракта
		currency_names_var = StringVar(frame_midd_2, value=self.currency_names)
		list_box_6 = Listbox(frame_midd_2, listvariable=currency_names_var, width=18, height=15)
		list_box_6.pack(side=LEFT, fill=Y, expand=0, padx=10)
		list_box_6.yview_scroll(number=1, what="units")
	
	def set_frame_bottom(self):
		...



# добавляем вертикальную прокрутку
# scrollbar = ttk.Scrollbar(frame_ontop_2, orient=VERTICAL, command=tree.yview)
# scrollbar.pack(side=RIGHT, fill=Y)
# tree["yscrollcommand"]=scrollbar.set

# from YaGPT
# чтобы размер окна менялся в зависимости от дисплея
# import tkinter as tk
# import time
#
# class Main(tk.Tk):
#     def resize_window(self, width, height):
#         self.wm_geometry(width + "x" + height)
#
#     def update_window(self):
#         width = int(self.winfo_screenwidth()) - 10
#         height = int(self.winfo_screenheight()) - 10
# 	self.resize_window(str(width), str(height))
#
# def run(self):
# 	self.after(100, self.update_window)
# 	self.update_window()
#
# def start(self):
# 	self.run()
#
# if name == “main”:
# root = Main()
# root.title(“Resize Window”)
# root.start()
# ОЧЕНЬ ПОЛЕЗНЫЙ МАТЕРИАЛ для управления размерами окна - https://learn-codes.org/php/525387-tkinter-auto-resize-window
# еще один материал - https://syntaxbug.com/d75296bcba/
# https://python.hotexamples.com/examples/tkinter/Tk/winfo_screenwidth/python-tk-winfo_screenwidth-method-examples.html#google_vignette

