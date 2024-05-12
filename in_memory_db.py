import sqlite3

query = (""" select * from data_contract where lot_number = 80145; """)
conn= sqlite3.connect("data/sql_krd.db")
cur = conn.cursor()
result = cur.execute(query).fetchall()
print(result)

columns = [column[0] for column in cur.description]

conn_2 = sqlite3.connect(':memory:')
cur_2 = conn_2.cursor()
cur_2.execute(""" CREATE TABLE IF NOT EXISTS tmp_tab (
				  lot_number INT,
				  close_date INT,
				  contract_number TEXT,
				  contract_date INT,
				  contract_maker TEXT,
				  contract_keeper TEXT,
				  good_name TEXT,
				  supplier_unit TEXT,
				  good_count REAL,
				  unit TEXT,
				  unit_price REAL,
				  total_price REAL,
				  add_expenses REAL,
				  lottotal_price REAL,
				  currency TEXT)""")
cur_2.execute(
	"""INSERT INTO tmp_tab( lot_number,
				  close_date,
				  contract_number,
				  contract_date,
				  contract_maker,
				  contract_keeper,
				  good_name,
				  supplier_unit,
				  good_count, unit,
				  unit_price,
				  total_price,
				  add_expenses,
				  lottotal_price,
				  currency)
			SELECT a.lot_number,
				  a.close_date,
				  a.contract_number,
				  a.contract_date,
				  a.contract_maker,
				  a.contract_keeper,
				  a.good_name,
				  a.supplier_unit,
				  a.good_count, unit,
				  a.unit_price,
				  a.total_price,
				  a.add_expenses,
				  a.lottotal_price,
				  a.currency FROM data_contract AS a
				  where a.lot_number = 80145; """)

conn = sqlite3.connect(':memory:')
cur = conn.cursor()
res = cur.execute("""select * from tmp_tab;""").fetchall()
print(res)
