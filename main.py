from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox as mb
from utils.data_model import DataModel
from frames import create_dbasetable
from frames.select_frame import SelectFrame

class MyWindow:
	data_df = None
	
	def clicked_connect(self):
		"""эта функция вызывает метод open_file из класса Data_model модуля data_model.py"""
		self.datamodel.open_file()
	
	# def clicked_connect_contr(self):
	# 	print('We go to open_file_contr')
	# 	self.datamodel.open_file_contr()
	
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
		"""здесь будет подготовка основного датафрейма и словарей"""
		DataModel(self).prepare_dicts()
	
	def exit(self):
		""" Здесь выскакивет диалоговое окно при нажатии на Выход"""
		choice = mb.askyesno("Выход из программы",
		                     "Вы действительно хотите выйти из программы?")
		if choice:
			self.root.destroy()
	
	def __init__(self, width, height, title="Анализ закупочных процессов", resizable=(True, True), data_df=None):
		self.root = Tk()
		self.font = font.Font(size=14, weight="normal")
		self.root.title(title)
		self.root.geometry(f"{width}x{height}")
		
		menu_bar = Menu(self.root)  # здесь шрифт не увеличивается
		
		file_menu = Menu(menu_bar, tearoff=0, font=('Courier', 12))
		settings_menu = Menu(menu_bar, tearoff=0, font=('Courier', 12))
		settings_menu.add_command(label='Загрузить файл с Лотами',
		                          command=self.clicked_connect)
		settings_menu.add_command(label='Загрузить файл с Контрактами',
		                          command=self.clicked_connect)
		file_menu.add_cascade(label="Загрузить файл Excell",
		                      menu=settings_menu)
		file_menu.add_separator()
		
		file_menu.add_command(label="Загрузить из Базы данных",
		                      command=self.load_sql_data)
		file_menu.add_separator()
		file_menu.add_command(label="Выход",
		                      command=self.exit)
		menu_bar.add_cascade(label="Загрузка и подготовка данных",
		                     menu=file_menu, background='Black',
		                     foreground='white')  # почему-то эта строка не работает
		self.root.config(menu=menu_bar)
		self.root.geometry("640x320")
		
		# Main Window
		
		self.notebook = ttk.Notebook()
		self.notebook.pack(fill=BOTH, expand=1)
		
		# Notebook Analytics Data
		# analytics_frame = ttk.LabelFrame(self.notebook).pack(fill=BOTH, expand=1)
		# self.notebook.add(analytics_frame, text="Аналитика данных")
		
		# Status Bar
		status_bar = Label(self.root, text="Готово", bd=1, relief=SUNKEN, anchor=W)
		status_bar.pack(side=BOTTOM, fill=X)
		# Progress Bar
		self.progress_bar = ttk.Progressbar(orient="horizontal", length=100, variable=status_bar, mode='indeterminate')
		self.progress_bar.pack(side=BOTTOM, fill=X)
		
		self.datamodel = DataModel(self)
		
		# Frames
		
		self.root.mainloop()


if __name__ == "__main__":
	root = MyWindow(1900, 542, "Анализ закупочных процессов")
