from tkinter import *
from tkinter import Tk
def __init__(self, num_rows, num_cols, best_possible):
	self.rows = num_rows
	self.cols = num_cols
	self.expectedBest = best_possible
	# create the root and the canvas
	root = Tk()
	# local function to bind/unbind events
	self.bind = root.bind
	self.unbind = root.unbind
	# local function to change title
	self.updateTitle = root.title
	# local function to change cursor
	self.updateCursor = lambda x: root.config(cursor=x)
	# local function to start game
	self.start = root.mainloop
	# get screen width and height
	ws = root.winfo_screenwidth()
	hs = root.winfo_screenheight()
	
	# fix scaling for higher resolutions
	if max(self.canvasWidth / ws, self.canvasHeight / hs) < 0.45:
		self.scale = 2
	
	self.canvas = Canvas(root, width=self.canvasWidth, height=self.canvasHeight)
	self.canvas.pack()
	# calculate position x, y
	x = (ws - self.canvasWidth) // 2
	y = (hs - self.canvasHeight) // 2
	root.geometry('%dx%d+%d+%d' % (self.canvasWidth, self.canvasHeight, x, y))
	root.resizable(width=0, height=0)
	self.init()
	# set up keypress events
	#root.bind, "<Клавиша>"(самостоятельно.Нажата клавиша)
