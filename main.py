# Использовать материалы из https://docs.python.org/3/library/sqlite3.html#how-to-guides
# материалы по tkinter pythcn - https://www.pythontutorial.net/tkinter/

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from utils.data_model import DataModel
from frames import create_dbasetable
from frames.select_frame import SelectFrame


class MyWindow:
	data_df = None
	
	def clicked_connect(self):
		"""эта функция вызывает метод open_file из класса Data_model модуля data_model.py"""
		self.datamodel.open_file()
	
	def load_sql_data(self):
		""" Прочесть данные из базы SQL"""
		print('Сейчас заходим в DataModel(self).open_from_db()')
		DataModel(self).open_from_db()
		print('Мы вернулись!!!')
		self.select_frame = SelectFrame(self)
		analytics_frame = ttk.LabelFrame(self.notebook)
		analytics_frame.pack(fill=BOTH, expand=1)
		self.notebook.add(analytics_frame, text="Аналитика данных")
		print('После вывода картинки - мы сейчас здесь! (т.е в бесконечном цикле')
		"""здесь должна быть подготовка основных аналитических данных и их визуализация в окне Аналитика"""
		DataModel(self).prepare_analytic_data()
	
	def exit(self):
		""" Здесь выскакивет диалоговое окно при нажатии на Выход"""
		choice = mb.askyesno("Выход из программы",
		                     "Вы действительно хотите выйти из программы?")
		if choice:
			self.root.destroy()
	
	def __init__(self, title="Анализ закупочных процессов"):
		self.root = tk.Tk()
		# self.font = font.Font(size=14, weight="normal")
		self.root.title(title)
		# window_width = 800
		# window_height = 600
		self.screen_width = self.root.winfo_screenwidth()
		self.screen_height = self.root.winfo_screenheight()
		
		# center_x = int(screen_width / 2 - window_width / 2)
		# center_y = int(screen_height / 2 - window_height / 2)
		self.root.geometry(f"{self.screen_width}x{self.screen_height}")
		# self.root.attributes('-alpha', 1.0)
		
		menu_bar = Menu(self.root)  # здесь шрифт не увеличивается
		menu_bar.config(font=("Helvetica", 14))
		
		file_menu = Menu(menu_bar, tearoff=0, font=('Courier', 12))
		settings_menu = Menu(menu_bar, tearoff=0, font=('Courier', 12))
		settings_menu.add_command(label='Загрузить файл с Лотами',
		                          command=self.clicked_connect)
		settings_menu.add_command(label='Загрузить файл с Контрактами',
		                          command=self.clicked_connect)
		file_menu.add_cascade(label="Загрузить файл Excell",
		                      menu=settings_menu)
		file_menu.add_separator()
		
		file_menu.add_command(label="Получить основные данные",
		                      command=self.load_sql_data)
		file_menu.add_separator()
		file_menu.add_command(label="Выход",
		                      command=self.exit)
		menu_bar.add_cascade(label="Загрузка и подготовка данных",
		                     menu=file_menu, background='Black',
		                     foreground='white')  # почему-то эта строка не работает
		self.root.config(menu=menu_bar)
		
		# Main Window
		
		self.notebook = ttk.Notebook(self.root)
		self.notebook.pack(fill=BOTH)
		
		# Notebook Analytics Data
		# analytics_frame = ttk.LabelFrame(self.notebook).pack(fill=BOTH, expand=1)
		# self.notebook.add(analytics_frame, text="Аналитика данных")
		
		# Status Bar
		status_bar = ttk.Label(self.root, text="Готово", relief=SUNKEN, anchor=W)
		status_bar.pack(side=BOTTOM, fill=X)
		# Progress Bar
		self.progress_bar = ttk.Progressbar(orient="horizontal", length=100, variable=status_bar, mode='indeterminate')
		self.progress_bar.pack(side=BOTTOM, fill=X)
		
		self.datamodel = DataModel(self)
		
		# Frames
		
		self.root.mainloop()


if __name__ == "__main__":
	root = MyWindow(title="Анализ закупочных процессов")

