# в этот файд sql_queryes необходимо перенести все строки кода, связанные с работой с Базой данных sql_krd_new.db

# Полезная ссылка - https://www.guru99.com/ru/python-tutorials.html

import sqlite3

query = (""" select lot_number, winner_name from data_contract where lot_number IN
			(select lot_number, winner_name from data_kp where close_date >= '2023-01-01')
			""")
# здесь надо использовать один из JOINов
conn = sqlite3.connect("data/sql_krd_new.db")
cur = conn.cursor()
res = cur.execute(query).fetchall()
len_res = len(res)
conn.close()

print(res)
print('Количество элементов', len_res)