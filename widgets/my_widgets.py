import tkinter as tk
from utils.styles import label_style, button_style, entry_style


class MyLabel(tk.Label):
    def __init__(self, parent, **kwargs):
        kwargs.update(label_style)
        super().__init__(parent, **kwargs)


class MyButton(tk.Button):
    def __init__(self, parent, **kwargs):
        kwargs.update(button_style)
        super().__init__(parent, **kwargs)


class MyEntry(tk.Entry):
    def __init__(self, parent, placeholder, **kwargs):
        kwargs.update(entry_style)
        super().__init__(parent, **kwargs)
        self.placeholder = placeholder
        self.insert(0, placeholder)
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)
        parent.bind("<Configure>", self._resize)

    def _clear_placeholder(self, event=None):
        if self.get() == self.placeholder:
            self.delete(0, "end")

    def _add_placeholder(self, event=None):
        if not self.get():
            self.insert(0, self.placeholder)

    def _resize(self, event):
        # Dynamically adjust the width of the entry widget
        new_width = event.width
        print(new_width)
        self.config(width=new_width-100)