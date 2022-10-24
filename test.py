from tkinter import *
from tkinter import filedialog as tkf
from tkinter import ttk
import base
import os
from functools import partial
from PIL import ImageTk, Image


class AppScreen():
    def __init__(self, master, image):
        self.master = master
        self.image = PhotoImage(file=image)


class App(Tk):
    def __init__(self):
        super().__init__()
        self.entry1 = Entry(self)
        self.folder_path = ''
        self.program_location = os.path.dirname(os.path.abspath(__file__))
        self.spec_name = ''
        self.iconbitmap(
            self.program_location + r"\Interface\top_left.ico")
        self.current_screen_number = 0
        self.title("Cuadp Analyzer")
        self.resizable(False, False)

        self.menubar = Menu(self, bd=-2)
        self.file_menu = Menu(self.menubar, tearoff=0, bg="white", fg="black", bd=30)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.config(menu=self.menubar, bg='#F2E500')
        self.file_menu.add_command(label="Open", accelerator="Ctrl+O")

        self.screen = Canvas(self, bg="white", width=1000, height=400, bd=-2)
        self.screen.pack()

    def set_screen(self, screens):
        self.screens = screens

    def display_screen(self):
        self.active_screen = self.screens
        self.screen.delete("all")
        self.screen.create_image((400, 200), image=self.active_screen.image)
if __name__ == '__main__':
    print(os.path.dirname(os.path.abspath(__file__)))
    app = App()
    a1 = AppScreen(app,
                   r'c:\Users\uic00691\PycharmProjects\Cuadp Program DemoV2.1(Adapted Interface)\Interface\bg2.png')
    app.set_screen(a1)
    app.mainloop()
