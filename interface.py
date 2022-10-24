from tkinter import *
from tkinter import ttk
from tkinter import filedialog


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.folder_location = ''
        self.title("CUADP Program")
        self.minsize(300, 300)
        self.wm_iconbitmap(r"c:\Users\uic00691\PycharmProjects\Cuadp Program Demo1\icon.png")

        self.labelFrame = ttk.LabelFrame(self, text="Open File")
        self.labelFrame.grid(column=0, row=1, padx=150, pady=20)

        self.button_browse()

    def button_browse(self):
        self.button = ttk.Button(self.labelFrame, text="Select Project work location", command=self.fileDialog)
        self.button.grid(column=100, row=1)
        #self.button.configure(background='#e3ad41')


    def fileDialog(self):
        #self.filename = filedialog.askopenfilename(initialdir="/", title="Select A File", filetype=
        #(("jpeg files", "*.jpg"), ("all files", "*.*")))
        self.folder_location = filedialog.askdirectory()
        self.label = ttk.Label(self.labelFrame, text="")
        self.label.grid(column=1, row=2)
        self.label.configure(text=self.folder_location)
        print(self.folder_location)

