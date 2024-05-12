from tkinter import *

def Scankey(event):
    val = event.widget.get()
    if val == '':
        data = list
    else:
        data = []
        for item in list:
            if val.lower() in item.lower():
                data.append(item)
    Update(data)

def Update(data):
    listbox.delete(0, 'end')
    # put new data
    for item in data:
        listbox.insert('end', item)

list = ('C', 'C++', 'Java',
        'Python', 'Perl',
        'PHP', 'ASP', 'JS',
        'JVC', 'Toyota', 'Beatles',
        'Deep Purple', 'Middleware', 'Compare',
        'Komparison', 'Uriah Heep')

tk = Tk()

listbox = Listbox(tk)
listbox.pack()
Update(list)

entry = Entry(tk)
entry.pack()
entry.bind('<KeyRelease>', Scankey)

tk.mainloop()
