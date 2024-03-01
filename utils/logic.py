import pandas as pd
import numpy as np
from collections import Counter
from utils.functions import del_nan, get_unique_only


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


def upload_to_sql_df(df, conn, table):
	df.to_sql(table, conn, if_exists="append", index=True)
	tab = table
	cur = conn.cursor()
	cur.executescript(
		'''UPDATE table SET close_date = substr(close_date, 7, 4)
	                || '-' || substr(close_date, 4, 2) || '-' || substr(close_date, 1, 2);
	UPDATE table SET open_date = substr(open_date, 7, 4) || '-' || substr(open_date, 4, 2) || '-' || substr(open_date, 1, 2);''')
	
	conn.commit()


# Функция определяет номер квартала по дате
def quarter_of_date(date_tmp):
	quarter = (date_tmp.month - 1) // 3 + 1
	quarter = 'Q' + str(quarter) + '_' + date_tmp[6:10]
	return quarter


# В этом модуле идет подготовка основных укрупненных данных

def prep_basic_data(data_df):
	# Эта функция собирет в список (массив) только уникальные элементы
	# из датафрейма data_df вызываем все даты закрытия лотов
	date_strings = get_unique_only(list(data_df['Дата_закрытия_лота']))
	# получаем начальную и конечную даты
	earliest_date = min(date_strings)
	latest_date = max(date_strings)
	begend_date = [earliest_date, latest_date]
	return begend_date


def prepare_main_datas(data_df):
	# Подготовка базовых данных
	# Группировка data_df - суммы и средние значения сумм в разрезе валют
	# по дисциплинам Компании
	agg_sum = {'Сумма_контракта': ['sum', 'mean']}
	df_disc_sum = data_df.groupby(['Дисциплина', 'Валюты_контракта']).agg(agg_sum)
	# print(df_disc_sum)
	
	# Суммы контрактов (проработок) по проектам Компании в разрезе валют
	agg_sum = {'Сумма_контракта': ['sum', 'mean']}
	data_df.groupby(['Наименование_проекта', 'Валюты_контракта']).agg(agg_sum)
	
	# # Количество контрактов (проработок) в разрезе Дисциплин
	agg_func_count = {'Дисциплина': ['count']}
	data_df.groupby(['Дисциплина', 'Валюты_контракта']).agg(agg_func_count)
	
	# # а как это количество проработок делится между Исполителями?
	agg_func_count = {'Дисциплина': ['count']}
	data_actors_count = data_df.groupby(['Дисциплина', 'Исполнитель_МТО',
	                                     'Валюты_контракта']).agg(agg_func_count)
	
	# полученные значения возвращаем в вызывающий (data_model.py) модуль
	# sys.argv = [earliest_date, latest_date]
	
	# df_one = "data_df.loc[data_df[" + "Валюты_контракта" + ']=="UZS"]'
	# print(df_one)
	#
	# sys.df = df_one
	
	return df_disc_sum, data_actors_count
