import tkinter as tk
from widgets.my_widgets import MyLabel, MyButton
from utils.logic import on_button_click
from tkinter.ttk import Notebook


class MyFrame(tk.Frame):
    def __init__(self, parent, data, status_bar):
        super().__init__(parent)
        self.data = data  # SQL данные
        self.status_bar = status_bar

    def on_click(self):
        on_button_click(self.label)
        self.status_bar.config(text="Button clicked!")
        self.data_model.set_data("last_click", "button")



