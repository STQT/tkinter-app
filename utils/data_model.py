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

from utils.functions import prepare_main_datas, create_treeview_table
import sys

pd.options.display.float_format = '{:,.2f}'.format
import sqlite3


class DataModel:
	StringVar = ''
	
	def __init__(self, mywindow):
		self.frame_ontop_2 = None
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
				# откр/закр sql_krd.db перенести в functions.py
				conn = sqlite3.connect("data/sql_krd.db")
				cur = conn.cursor()
				cur.execute("DELETE FROM data_tmp")
				upload_to_sql_df(df, conn, "data_tmp")
				cur.executescript(
					"""INSERT INTO data_kp(lot_number, lot_status, discipline, project_name,
						open_date, close_date, actor_name, good_name,
						good_count, unit, supplier_qty, supplier_unit,
						winner_name, unit_price, total_price, currency)
					SELECT
					a.lot_number, a.lot_status, a.discipline, a.project_name,
					a.open_date, a.close_date, a.actor_name, a.good_name,
					a.good_count, a.unit, a.supplier_qty, a.supplier_unit,
					a.winner_name, a.unit_price, a.total_price, a.currency
					FROM data_tmp AS a;"""
				)
				conn.commit()
			else:
				# clean_contr и clean_data объединить в одной функции
				df = clean_contr_data_from_xls(file_path)
				conn = sqlite3.connect("data/sql_krd.db")
				cur = conn.cursor()
				cur.execute("DELETE FROM data_contr_tmp")
				df.to_sql("data_contr_tmp", conn, if_exists="append", index=True)
				cur.executescript(
					'''UPDATE data_contr_tmp SET close_date = substr(close_date, 7, 4)
								|| '-' || substr(close_date, 4, 2) || '-' || substr(close_date, 1, 2);
				UPDATE data_contr_tmp SET contract_date = substr(contract_date, 7, 4)
				|| '-' || substr(contract_date, 4, 2) || '-' || substr(contract_date, 1, 2);''')
				
				cur.execute(
					'''insert into data_contract(lot_number, close_date, contract_number,
					  contract_date, contract_maker, contract_keeper, good_name,
					  supplier_unit, count, unit, unit_price, total_price,
					  add_expenses, lottotal_price, currency)
					  select
					  a.lot_number, a.close_date, a.contract_number,
					  a.contract_date, a.contract_maker, a.contract_keeper, a.good_name,
					  a.supplier_unit, a.count, a.unit, a.unit_price, a.total_price,
					  a.add_expenses, a.lottotal_price, a.currency
					  from data_contr_tmp as a;'''
				)
				cur.execute('DELETE FROM data_contract WHERE count = 0.0')
				conn.commit()
			self.progress.stop()
		
		threading.Thread(target=real_traitement).start()
	
	def open_from_db(self):
		start_time = time.time()
		conn = sqlite3.connect("data/sql_krd.db")
		data_df = pd.read_sql("select * from data_kp", conn)
		self.mywindow.data_df = data_df # а нужно ли нам в дальнейшем data_df или обойдемся SQL Query?
		print('Возвращаемся в место вызова')
		
		# Обращаемся к модулю подготовки основных данных
		str_query_1 = ("""
						select discipline, currency, sum(total_price) as sum_prices,
						avg(total_price) as avg_prices from data_kp where currency not null
						group by discipline, currency;
						""")
		df_query_1 = prepare_main_datas(str_query_1)  # методом Treeview разместить в окне
		print(df_query_1)
		
		str_query_2 = ("""
						select discipline, currency, count(DISTINCT(lot_number)) as lots_count
						from data_kp where currency not null group by discipline, currency;
						""")
		df_query_2 = prepare_main_datas(str_query_2)
		print(df_query_2)
		# print(df_query_2) далее необходимо этот датафрейм разместить в окне
		
		# Здесь требуется доработка. Но прежде чем это выводить в аналит окне, необходио
		# параметры выбрать "кликом" на первом окне - Основные данные
		
		str_query_3 = ("""select discipline, actor_name, currency, count(distinct(lot_number)) as lot_count
						from data_kp where currency IS NOT NULL AND discipline IS NOT NULL
						group by discipline, actor_name, currency;""")
		df_query_3 = prepare_main_datas(str_query_3)
		print(df_query_3)
		# обращаемся в функции functions.create_treeview_table()
		param1, param2 = create_treeview_table(df=df_query_3)
		print(param1, param2)
	
		tree = ttk.Treeview(self.frame_ontop_2, columns=param1, show='headings')
		tree.pack(side=LEFT, fill=BOTH, expand=1)
		
		for i in range(len(param1)):
			tree.heading(i, text=param1[i], anchor=W)
			tree.column(i, stretch=NO, width=70)

		for param in param2:
			tree.insert("", END, values=param)
	
	def prepare_analytic_data(self):
		# здесь находим все контракты, которые были заключены (???) без конкурсных проработок
		# и выводим в файл Excel
		conn = sqlite3.connect("data/sql_krd.db")
		cur = conn.cursor()
		# здесь нужно использовать параметризацию с датами
		cur.execute("""
					SELECT distinct(data_contract.lot_number), data_contract.close_date,
						data_contract.contract_maker, data_contract.contract_keeper,
						data_contract.good_name, data_contract.good_count, data_contract.unit,
						data_contract.unit_price, data_contract.total_price, data_contract.currency
					FROM data_contract
					WHERE data_contract.close_date >= '2023-01-01' AND
					data_contract.lot_number NOT IN
					(SELECT distinct(lot_number) FROM data_kp WHERE close_date >= '2023-01-01')
					ORDER BY data_contract.contract_keeper;
					""")
		columns = [column[0] for column in cur.description]
		values = cur.fetchall()
		row_dict = {}
		k = 0
		for column in columns:
			list_tmp = []
			for value in values:
				list_tmp.append(value[k])
			row_dict[column] = list_tmp
			k += 1
		df_1 = pd.DataFrame(row_dict)
		print('df_1 = ', df_1)
		df_1.to_excel('contracts_without_KP.xlsx')
