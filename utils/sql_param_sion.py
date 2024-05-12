# Источник - https://docs.python.org/3/library/sqlite3.html#sqlite3-howtos

import sqlite3

conn = sqlite3.connect("data/sql_krd.db")
cur = conn.cursor()
cur.execute("""select count(distinct lot_number) from data_kp
            where project_name = 'Бойсун ГПЗ (ЕРС)'
            and winner_name = 'М5-ЭКСПОРТ ООО';""")

print(cur.fetchall())

conn.close()

