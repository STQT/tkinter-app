import tkinter as tk
from widgets.my_widgets import MyEntry, MyLabel


class AdditionalFrame(tk.Frame):
    def __init__(self, parent, data_model, status_bar):
        super().__init__(parent)
        self.data_model = data_model
        self.status_bar = status_bar

        self.entry = MyEntry(self, placeholder="Введите что-нибудь и нажмите Enter...")
        self.entry.pack()
        self.entry.bind("<Return>", self.on_enter_press)
        self.entry.bind("<Control-a>", self.select_all)
        self.entry.bind("<Control-A>", self.select_all)  # for caps lock

        self.output_label = None  # Placeholder for the label
        self.set_minimum_window_size()

    def on_enter_press(self, event):
        text = self.entry.get()
        if text and text != self.entry.placeholder:
            if not self.output_label:
                self.output_label = MyLabel(self, text=text)
                self.output_label.pack()
            else:
                self.output_label.config(text=text)
            self.status_bar.config(text="Введено: " + text)
            self.data_model.set_data("last_text", text)
        else:
            self.status_bar.config(text="Ничего не введено")

    def select_all(self, event):
        self.entry.select_range(0, tk.END)
        return 'break'  # prevent the default binding action

    def set_minimum_window_size(self):
        min_width = 640  # Minimum width for the window
        min_height = 320 # Minimum height for the window
        self.master.geometry(f"{min_width}x{min_height}")