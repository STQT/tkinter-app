import tkinter as tk
from tkinter import ttk
# from PIL import Image,ImageTk
import ctypes #Python and C language can be mixed
# Tell the operating system to use the dpi adaptation of the program itself
ctypes.windll.shcore.SetProcessDpiAwareness(1)

class mytkinter(tk.Tk):
    width=800
    height=600
    ROW=10
    COL=10
    first_load=True
    # def __init__(self):
    # super().__init__()


    def setupUi(self):
        self.config(bg='#666888', bd=0)
        self.title("YOLOv5 detection")
        screen_width = self.winfo_screenwidth() # computer screen width
        screen_height = self.winfo_screenheight()
        print(screen_width, screen_height)
        center_geometry = [int(screen_width / 2 - self.width / 2), int(screen_height / 2 - self.height / 2)]
        geometry_str = "{}x{}+{}+{}".format(self.width, self.height, center_geometry[0], center_geometry[1])
        print(geometry_str)
        self.geometry(geometry_str)

        # canvas
        self.cv = tk.Canvas(self, bg='snow')

        # self. style_1 = ttk. Style()
        # self.style_1.configure("TLabel",foreground='black',background='ivory')
        self.tab_main = ttk.Notebook(self.cv)
        # self.tab_main.pack(expand=1,fill='both')#This code is very important


        self.tab1 = tk.Frame(self.tab_main, bg='snow')
        self.tab1.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.9)
        self.tab_main.add(self.tab1, text='image detection')

        self.tab2 = tk.Frame(self.tab_main, bg='ivory')
        self.tab2.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.9)
        self.tab_main.add(self.tab2, text='video detection')

        self.tab3 = tk.Frame(self.tab_main, bg='#eeebbb')
        self.tab3.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.9)
        self.tab_main.add(self.tab3, text='camera detection')

        self.tab4 = tk.Frame(self.tab_main, bg='#666888')
        self.tab4.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.9)
        self.tab_main.add(self.tab4, text='set')

        #tab1
        self.VLabel1 = self.myViewLabel(self.tab1, 0.005, 0.1, 0.49, 0.9)
        self.VLabel2 = self.myViewLabel(self.tab1, 0.505, 0.1, 0.49, 0.9)

        # tab2
        self.VLabel3 = self.myViewLabel(self.tab2, 0.005, 0.1, 0.49, 0.9)
        self.VLabel4 = self.myViewLabel(self.tab2, 0.505, 0.1, 0.49, 0.9)

        # tab3
        self.VLabel5 = self.myViewLabel(self.tab3, 0.005, 0.1, 0.49, 0.9)
        self.VLabel6 = self.myViewLabel(self.tab3, 0.505, 0.1, 0.49, 0.9)

        #tab4
        self.btn1=tk.Button(self.tab4,text='select weight',bd=0,bg='black',fg='white')
        self.btn1.place(relx=0.01,rely=0.05,width=100,height=30)
        self.label1=tk.Label(self.tab4,text="yolov5s.pt")
        self.label1.place(relx=0.01,x=105,rely=0.05,relwidth=0.98,width=-105,height=30)

        self.label2 = tk.Label(self.tab4, text="image size", bd=0, bg='black', fg='white')
        self.label2.place(relx=0.01,rely=0.05,y=50,width=100,height=30)
        self.var2 = tk.StringVar()
        self.entry2=tk.Entry(self.tab4,textvariable=self.var2)
        self.entry2.place(relx=0.01,x=105,rely=0.05,y=50,relwidth=0.48,width=-105,height=30)
        self.var2.set("640")

        self.label3 = tk.Label(self.tab4, text="confidence threshold", bd=0, bg='black', fg='white')
        self.label3.place(relx=0.51, rely=0.05, y=50, width=100, height=30)
        self.var3 = tk.StringVar()
        self.entry3 = tk.Entry(self.tab4, textvariable=self.var3)
        self.entry3.place(relx=0.51, x=105, rely=0.05, y=50, relwidth=0.48, width=-105, height=30)
        self.var3.set("0.25")

        self.label4 = tk.Label(self.tab4, text="iou threshold", bd=0, bg='black', fg='white')
        self.label4.place(relx=0.01, rely=0.05, y=100, width=100, height=30)
        self.var4 = tk.StringVar()
        self.entry4 = tk.Entry(self.tab4, textvariable=self.var4)
        self.entry4.place(relx=0.01, x=105, rely=0.05, y=100, relwidth=0.48, width=-105, height=30)
        self.var4.set("0.45")

        self.label5 = tk.Label(self.tab4, text="maximum number of targets", bd=0, bg='black', fg='white')
        self.label5.place(relx=0.51, rely=0.05, y=100, width=100, height=30)
        self.var5 = tk.StringVar()
        self.entry5 = tk.Entry(self.tab4, textvariable=self.var5)
        self.entry5.place(relx=0.51, x=105, rely=0.05, y=100, relwidth=0.48, width=-105, height=30)
        self.var5.set("100")

        self.label6 = tk.Label(self.tab4, text="detection device selection", bd=0, bg='black', fg='white')
        self.label6.place(relx=0.01, rely=0.05, y=150, width=100, height=30)
        self.var6 = tk.StringVar()
        self.entry6 = tk.Entry(self.tab4, textvariable=self.var6)
        self.entry6.place(relx=0.01, x=105, rely=0.05, y=150, relwidth=0.48, width=-105, height=30)
        self.var6.set("0")
        self.btn2=tk.Button(self.tab4,text="save settings", bd=0, bg='black', fg='white')
        self.btn2.place(relx=0.51, rely=0.05, y=150, relwidth=0.48, height=30)

    def myViewLabel(self,master,relx,rely,relwidth,relheight):#custom label, used to display pictures, can zoom in and out of pictures
        label=tk.Label(master,bg='#666888',bd=0)
        label.place(relx=relx,rely=rely,relwidth=relwidth,relheight=relheight)
        # self.label.bind("<Double-Button-1>",lambda a:mytkinter().show_toplevel(self))
        return label



# top=mytkinter()
# # top.config(bg='red')
# top. mainloop()