import pandas as pd


def del_nan(list_name):
	L1 = [item for item in list_name if not (pd.isnull(item)) is True]
	L1, list_name = list_name, L1
	return list_name


def get_unique_only(st):
	# Empty list
	lst1 = []
	count = 0
	# traverse the array
	for i in st:
		if i != 0:
			if i not in lst1:
				count += 1
				lst1.append(i)
	return lst1


# Функция "обрезки" строки до нужного символа
def cut_list(lstt_act):
	last_act = []
	for lst_act in lstt_act:
		try:
			if lst_act != 'nan':
				last_act.append(lst_act.partition(' (')[0])
		except AttributeError:
			continue
	return last_act

# class OpenListbox(select_frame):
#     print('Мы в модуле FUNCTIONS')
#     list =''
#     def __init__(self, master=None, *args, **kwargs):
#         self.data = {}
#         # self.frame_middle = frame_middle
#         self.mywindow = master
#
#     def srch_lisbox_item(list):
#         def Scankey(event):
#             val = event.widget.get()
#             if val == '':
#                 data = list
#             else:
#                 data = []
#                 for item in list:
#                     if val.lower() in item.lower():
#                         data.append(item)
#             Update(data)
#
#         def Update(data):
#             listbox.delete(0, 'end')
#             # put new data
#             for item in data:
#                 listbox.insert('end', item)
#
#         # list = ('C', 'C++', 'Java',
#         #         'Python', 'Perl',
#         #         'PHP', 'ASP', 'JS',
#         #         'JVC', 'Toyota', 'Beatles',
#         #         'Deep Purple', 'Middleware', 'Compare',
#         #         'Komparison', 'Uriah Heep')
#
#         listbox = Listbox(mywindow)
#         listbox.pack()
#         Update(list)
#
#         entry = Entry(mywindow)
#         entry.pack()
#         entry.bind('<KeyRelease>', Scankey)
