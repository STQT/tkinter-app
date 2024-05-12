import pandas as pd
import sqlite3
from tkinter import *
from tkinter import ttk


def del_nan(list_name):
	L1 = [item for item in list_name if not (pd.isnull(item)) is True]
	L1, list_name = list_name, L1
	return list_name


def get_unique_only(st):
	# Empty list
	lst1 = []
	count = 0
	# traverse the array
	for i in st:
		if i != 0:
			if i not in lst1:
				count += 1
				lst1.append(i)
	return lst1


# Функция "обрезки" строки до нужного символа
def cut_list(lstt_act):
	last_act = []
	for lst_act in lstt_act:
		try:
			if lst_act != 'nan':
				last_act.append(lst_act.partition(' (')[0])
		except AttributeError:
			continue
	return last_act


def calc_indicators(query):
	conn = sqlite3.connect("data/sql_krd_new.db")
	cur = conn.cursor()
	res = cur.execute(query).fetchall()
	return res


def prepare_main_datas(sql_query=None):
	# Суммы и средние значения контрактов в разрезе Дисциплин и валют контрактов
	# материал по работе SQLite_Python заимствован из
	# https://sky.pro/wiki/sql/preobrazovanie-rezultatov-zaprosa-sqlite-v-slovar/
	conn = sqlite3.connect("data/sql_krd_new.db")
	cur = conn.cursor()
	cur.execute(sql_query)
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
	df = pd.DataFrame(row_dict)
	return df


def create_treeview_table(df):
	columns = df.columns
	print('Our DF columns is ', columns)
	list_of_rows = []
	print('df.shape =', df.shape)
	for i in range(df.shape[0]):
		list_of_rows.append(df.T[i].tolist())
	param1 = columns
	param2 = list_of_rows
	return param1, param2

# функция параметризации запроса
def param_query(qry):
	conn = sqlite3.connect("data\sql_krd.db")
	cur = conn.cursor()
	cur.execute(qry)
	
	print(cur.fetchall())
	
	conn.close()

def scroll_box(scroll_param1, scroll_param2):
	scrollbar = ttk.Scrollbar(scroll_param2, orient=VERTICAL, command=scroll_param1.yview)
	scrollbar.pack(side=RIGHT, fill=Y, anchor=E)
	scroll_param1["yscrollcommand"] = scrollbar.set
	
	


