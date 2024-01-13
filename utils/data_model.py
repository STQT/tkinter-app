from tkinter import filedialog as fd
import pandas as pd


class DataModel:
    def __init__(self):
        self.data = {}

    def set_data(self, key, value):
        self.data[key] = value

    def get_data(self, key):
        return self.data.get(key, None)
    
    def open_file(self):
        wanted_files = (('Data files', '*.xlsx; *.csv'),
                        ('All', '*.*'))
        file_name = fd.askopenfilename(initialdir="D:/", title="Find a File",
                                       filetypes=wanted_files)
        excel_data_df = pd.read_excel(file_name)
        print(excel_data_df)
    