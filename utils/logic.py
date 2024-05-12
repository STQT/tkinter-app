import pandas as pd
import numpy as np
from collections import Counter
from utils.functions import del_nan, get_unique_only
from datetime import datetime
import sqlite3


def del_double_rows(basic_df):
	number_lots = del_nan(set(basic_df['lot_number']))
	for number_lot in number_lots:
		df_vrem = basic_df.loc[basic_df['lot_number'] == number_lot]
		if len(df_vrem) > 1:
			list_tup = []
			for ind in range(len(df_vrem)):
				ssl = df_vrem.iloc[[ind][0]].to_list()
				ssl = tuple(ssl)
				list_tup.append(ssl)
			c = Counter(list_tup)
			if set(c.values()) == {1}:
				continue
			else:
				list_unique_tup = set(list_tup)
				df_vrem = pd.DataFrame(list_unique_tup, columns=basic_df.columns)
				# удаляем из excel_data_df строки по номеру лота (number_lot)
				basic_df = basic_df[basic_df['lot_number'] != number_lot]
				basic_df = pd.concat([basic_df, df_vrem], ignore_index=True)
	return basic_df


def clean_data_from_xls(file):
	# start_time = time.time()
	
	dict_names = {'Номер лота': 'lot_number',
	              'Статус лота': 'lot_status',
	              'Дисциплина': 'discipline',
	              'Наименование проекта': 'project_name',
	              'Дата открытия лота': 'open_date',
	              'Дата закрытия лота': 'close_date',
	              'Исполнитель МТО (Ф.И.О.)': 'actor_name',
	              'Наименование ТМЦ': 'good_name',
	              'Количество ТМЦ': 'good_count',
	              'Ед. изм. ТМЦ': 'unit',
	              'Кол-во поставщика': 'supplier_qty',
	              'Ед.изм. поставщика': 'supplier_unit',
	              'Присуждено контрагенту': 'winner_name',
	              'Цена': 'unit_price',
	              'Сумма контракта': 'total_price',
	              'Валюты контракта': 'currency'}
	
	excel_data_df = pd.read_excel(file)
	excel_data_df = excel_data_df.rename(columns=dict_names)
	print('Переименованный файл')
	print(excel_data_df.columns)
	
	# заменим в числовых полях excel_data_df все отсутствующие данные (nan) на ноль (0)
	excel_data_df['good_count'] = excel_data_df['good_count'].replace(np.nan, 0)
	excel_data_df['total_price'] = excel_data_df['total_price'].replace(np.nan, 0)
	excel_data_df['supplier_qty'] = excel_data_df['supplier_qty'].replace(np.nan, 0)
	excel_data_df['unit_price'] = excel_data_df['unit_price'].replace(np.nan, 0)
	
	df = del_double_rows(excel_data_df)
	return df


def clean_contr_data_from_xls(file_path):
	# Создадим словарь наимеований столбцов
	dict_contract = {'Номер лота': 'lot_number', 'Дата завершения лота': 'close_date',
	                 'Номер контракта/договора по этому лоту': 'contract_number',
	                 'Дата заключения контракта/договора': 'contract_date',
	                 'Исполнитель ДАК': 'contract_maker',
	                 'Наименование контрагента-владельца контракта/договора': 'contract_keeper',
	                 'Наименование товара': 'good_name', 'Ед.изм. поставщика': 'supplier_unit',
	                 'Кол-во': 'count', 'Ед. изм.': 'unit', 'Цена за единицу товара': 'unit_price',
	                 'Сумма товара': 'total_price', 'Доп. расходы': 'add_expenses',
	                 'Общая сумма контракта по лоту': 'lottotal_price', 'Валюта контракта/договора': 'currency'}
	
	contract_df = pd.read_excel(file_path)
	contract_df = contract_df.rename(columns=dict_contract)
	
	# в числовых полях датафрейма все NaN заменяем на нули
	contract_df['count'] = contract_df['count'].replace(np.nan, 0)
	contract_df['unit_price'] = contract_df['unit_price'].replace(np.nan, 0)
	contract_df['lottotal_price'] = contract_df['lottotal_price'].replace(np.nan, 0)
	contract_df['total_price'] = contract_df['total_price'].replace(np.nan, 0)
	contract_df['add_expenses'] = contract_df['add_expenses'].replace(np.nan, 0)
	
	df = del_double_rows(contract_df)
	return df


def upload_to_sql_df(df, conn, data_tmp):
	df.to_sql(data_tmp, conn, if_exists="append", index=True)
	cur = conn.cursor()
	cur.executescript(
		'''UPDATE data_tmp SET close_date = substr(close_date, 7, 4)
	                || '-' || substr(close_date, 4, 2) || '-' || substr(close_date, 1, 2);
	UPDATE data_tmp SET open_date = substr(open_date, 7, 4) || '-' || substr(open_date, 4, 2) || '-' || substr(open_date, 1, 2);''')
	
	conn.commit()


# Функция определяет номер квартала по дате
def quarter_of_date(date_tmp):
	quarter = (date_tmp.month - 1) // 3 + 1
	quarter = 'Q' + str(quarter) + '_' + date_tmp[6:10]
	return quarter


# В этом модуле идет подготовка основных укрупненных данных

def connect_to_database(db_name):
	# Эта функция собирет в список (массив) только уникальные элементы
	# из датафрейма data_df вызываем все даты закрытия лотов
	# date_strings = get_unique_only(list(data_df['close_date']))
	# получаем начальную и конечную даты
	conn = sqlite3.connect(db_name)
	cur = conn.cursor()
	min_date = cur.execute('SELECT min(close_date) FROM data_kp').fetchone()
	max_date = cur.execute('SELECT max(close_date) FROM data_kp').fetchone()
	beg_end_date = [min_date, max_date]
	
	return beg_end_date
