# Источник - https://github.com/STQT/tkinter-app/invitations
import time
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Notebook
from tkinter import font
from frames.additional_frame import AdditionalFrame
from frames.my_frame import MyFrame
from tkinter import messagebox as mb
from utils.data_model import DataModel


class MyWindow:
	def clicked_connect(self):
		"""эта функция вызывает метод open_file из класса Data_model модуля data_model.py"""
		self.datamodel.open_file()
	
	# def load_data(self):
	#     """ Пре"""
	#     sql_data = self.load_sql_data()
	
	def load_sql_data(self):
		""" Прочесть данные из базы SQL"""
		DataModel(self).open_from_db()
	
	def exit(self):
		""" Здесь выскакивет диалоговое окно при нажатии на Выход"""
		choice = mb.askyesno("Выход из программы",
		                     "Вы действительно хотите выйти из программы?")
		if choice:
			self.root.destroy()
	
	def __init__(self, width, height, title="Анализ закупочных процессов", resizable=(True, True), data_df=None):
		self.root = Tk()
		self.font = font.Font(family="Courier", size=14, weight="normal")
		self.root.title(title)
		self.root.geometry(f"{width}x{height}")
		
		menu_bar = Menu(self.root, font=("Courier", 14))  # здесь шрифт не увеличивается
		
		file_menu = Menu(menu_bar, tearoff=0, font=('Courier', 13))
		file_menu.add_command(label="Загрузить файл Excell",
		                      command=self.clicked_connect)
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
	root = MyWindow(900, 542, "Анализ закупочных процессов")
