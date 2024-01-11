import tkinter as tk

from frames.additional_frame import AdditionalFrame
from frames.my_frame import MyFrame
from utils.data_model import DataModel

def main():
    root = tk.Tk()
    root.title("Пример с шаблоном")
    data_model = DataModel()

    # Menu
    menu_bar = tk.Menu(root)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Выход", command=root.quit)
    menu_bar.add_cascade(label="Файл", menu=file_menu)
    root.config(menu=menu_bar)
    root.geometry("640x320")

    # Status Bar
    status_bar = tk.Label(root, text="Готово", bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # Frames
    frame = MyFrame(root, data_model, status_bar)
    frame.pack()

    additional_frame = AdditionalFrame(root, data_model, status_bar)
    additional_frame.pack(padx=30)

    root.mainloop()


if __name__ == "__main__":
    main()
