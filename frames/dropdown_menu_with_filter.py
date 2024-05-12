import tkinter as tk


class App(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		
		self.title('Example of a filtered listbox')
		
		# Full screen.
		# self.state('zoomed')
		
		# 3 rows x 2 columns grid.
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=0)
		self.grid_rowconfigure(0, weight=0)
		self.grid_rowconfigure(1, weight=1)
		self.grid_rowconfigure(2, weight=0)
		
		# Put the filter in a frame at the top spanning across the columns.
		frame = tk.Frame(self)
		frame.grid(row=0, column=0, columnspan=2, sticky='we')
		
		# Put the filter label and entry box in the frame.
		tk.Label(frame, text='Filter:').pack(side='left')
		
		self.filter_box = tk.Entry(frame)
		self.filter_box.pack(side='left', fill='x', expand=True)
		
		# A listbox with scrollbars.
		yscrollbar = tk.Scrollbar(self, orient='vertical')
		yscrollbar.grid(row=1, column=1, sticky='ns')
		
		xscrollbar = tk.Scrollbar(self, orient='horizontal')
		xscrollbar.grid(row=2, column=0, sticky='we')
		
		self.listbox = tk.Listbox(self)
		self.listbox.grid(row=1, column=0, sticky='nswe')
		
		yscrollbar.config(command=self.listbox.yview)
		xscrollbar.config(command=self.listbox.xview)
		
		# The current filter. Setting it to None initially forces the first update.
		self.curr_filter = None
		
		# All of the items for the listbox.
		
		# The initial update.
		self.on_tick()
	
	def on_tick(self):
		if self.filter_box.get() != self.curr_filter:
			# The contents of the filter box has changed.
			self.curr_filter = self.filter_box.get()
			
			# Refresh the listbox.
			self.listbox.delete(0, 'end')
			
			for item in self.items:
				if self.curr_filter in item:
					self.listbox.insert('end', item)
		
		self.after(250, self.on_tick)


App().mainloop()

items = ['Xaydari Fidoi Zohir Zoda (вн. 32214) (моб. +998900300222)',
         'Абдуахатов Камолиддин Шухратович (вн. 14674) (моб. +998990264441)',
         'Абдуганиев Шахбоз Алижонович (вн. 13283) (моб. +99899 0000536)',
         'Абдулин Азиз Рустам угли (моб. +998974641101)',
         'Абдуллаев Аббос Махмуд угли (вн. 34219) (моб. +998332081423)',
         'Абдуллаев Абдулазиз Алишер угли (вн. 19539) (моб. +99891 1357737)',
         'Абдуллаев Элёр Ихтиёрович (вн. 37034) (моб. +99897 1225550)',
         'Абдурахманов Ёркинбек Абдуназарович (вн. 37190) (моб. +99897 3740774)',
         'Абдурахмонов Бехзоджон Зайниддин угли (вн. 37756) (моб. 998997505775)',
         'Абдухамидов Илхомжон Акром угли (вн. 32216) (моб. +99895 3341996)',
         'Абдухафизов Фируз Фуркатович (вн. 38966) (моб. 998974474114)',
         'Абидов Алишер Хаётович (вн. 16395) (моб. +99890 6115775)',
         'Авазов Нодир Останкулович (вн. 34813) (моб. 998906677188)',
         'Адигамова Эмилия Эмильевна (моб. +99781403355)',
         'Адилов Аскар Равшанович (моб. +998885430696)',
         'Азамов Иброхимжон Икромжон угли (моб. +998943932244)',
         'Азамов Мухаммадюсуф (вн. 34465) (моб. 998900556515)',
         'Азизов Сардорбек Сарвар угли (вн. 14624) (моб. +998900011255)',
         'Азимов Лазизжон Сухробович (моб. +99888 0072272)',
         'Акбаралиев Жавохир Тохиржон угли (вн. 16361) (моб. +998993133155)']
