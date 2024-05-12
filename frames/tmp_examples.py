import sqlite3
from config

conn = sqlite3.connect('data/sql_krd_new.db')
cursor = conn.cursor()

# Используем транзакцию для открытия базы
try:
    conn.execute('BEGIN')
    cursor.execute(''' CREATE TABLE IF NOT EXISTS v_data_kp (
	            lot_number INTEGER, lot_status	TEXT, discipline TEXT,
	            project_name TEXT, open_date INTEGER, close_date INTEGER, actor_name TEXT,
	            good_name	TEXT, good_count REAL, unit	TEXT, supplier_qty REAL,
	            supplier_unit	TEXT, winner_name	TEXT, unit_price REAL,
	            total_price REAL,	currency TEXT)''')
    conn.execute('COMMIT')
except sqlite3.Error as e:
    conn.execute("ROLLBACK")
    print(f"Error: {e}")
    
# проверим запрос
# Выбираем всех пользователей
cursor = conn.cursor()
results = cursor.execute('''SELECT lot_number, actor_name, winner_name
              FROM v_data_kp where close_date > "2024-03-01"''')
results = cursor.fetchall()

# Преобразуем результаты в список словарей
actors_list = []
actor_dict = {}
for result in results:
  actor_dict = {
    'lot_number': result[0],
    'actor_name': result[1],
    'winner_name': result[2],
  }
actors_list.append(actor_dict)

# Выводим результаты
for actor in actors_list:
  print(actor)

# Закрываем соединение
conn.close()