from tkinter import *
from tkinter import filedialog as tkf
from tkinter import ttk
# import base
import os
# some_file.py
import sys

# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(0, 'Scripts/')
from Scripts import base
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
        self.program_location = os.path.dirname(os.path.abspath("__file__"))
        self.spec_name = ''
        self.iconbitmap(
            self.program_location + r"\Interface\top_left.ico")
        self.current_screen_number = 0
        self.title("Cuadp Analyzer")
        self.resizable(False, False)
        self.xml_file = ''
        self.standalone = False
        self.log_path = ''

        self.menubar = Menu(self, bd=-2)
        self.file_menu = Menu(self.menubar, tearoff=0, bg="white", fg="black", bd=-2)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.config(menu=self.menubar, bg='#F2E500', bd=10)
        self.file_menu.add_command(label="Open", command=self.file_open, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Add Xml", command=self.file_add, accelerator="Ctrl+A")
        self.bind_all("<Control-o>", self.file_open)
        self.bind_all("<Control-a>", self.file_add)

        self.submit_image = PhotoImage(
            file=self.program_location + r"\Interface\submit.png")
        self.question_mark_image = PhotoImage(
            file=self.program_location + r"\Interface\icon_small.png")
        self.start_image = PhotoImage(
            file=self.program_location + r"\Interface\start_app.png")

        self.screen = Canvas(self, bg="white", width=1008, height=400, bd=-2)
        self.right_frame = Frame(self, width=150, height=100, bd=-5)
        self.right_frame.pack_propagate(0)
        self.start_program_cond = False
        # ---------------------------------------------- Project Location-----------------------------------------------
        project_location_space = Frame(self.right_frame, bg='white', width=200, height=320, bd=-2)
        project_location_space.pack_propagate(0)
        project_location_space.pack()
        project_location_row = Frame(project_location_space)
        project_location_slot = Button(project_location_row,
                                       image=self.question_mark_image,
                                       width=35, height=35,
                                       highlightthickness=0,
                                       bd=0,
                                       command=self.use_item)
        item_name_1 = StringVar(project_location_row)
        self.item_label_vars = item_name_1
        project_location_row.pack(side=TOP)
        project_location_slot.pack()

        # -------------------------------------------------Project Entry------------------------------------------------

        self.right_frame.place(rely=1.0, relx=1.0, x=-475, y=-280, anchor=NE)
        self.name_label_prj = Label(self, bg='white', text="Project location")
        self.name_label_prj.place(rely=1.0, relx=1.0, x=-430, y=-250, anchor=SE)
        self.entry_project = Entry(self, textvariable='ProjectLocation', width='60')
        self.entry_project.place(rely=1.0, relx=1.0, x=-40, y=-250, anchor=SE)

        # -----------------------------------------------Spec Entry-----------------------------------------------------

        self.name_label_spec = Label(self, bg='white', text="Specification Name")
        self.name_label_spec.place(rely=1.0, relx=1.0, x=-410, y=-150, anchor=SE)
        self.entry_spec = Entry(self, textvariable='SpecName', width='60')
        self.entry_spec.place(rely=1.0, relx=1.0, x=-40, y=-150, anchor=SE)
        self.submit = Button(self,
                             image=self.submit_image,
                             width=30, height=30,
                             highlightthickness=0,
                             bd=0,
                             command=self.value_get)
        self.submit.place(rely=1.0, relx=1.0, x=-540, y=-142, anchor=SE)

        self.button_start = Button(self,
                                   image=self.start_image,
                                   width=60, height=60,
                                   highlightthickness=0,
                                   bd=0,
                                   # command=self.start_program
                                   command=self.start_program)
        self.var = IntVar()

        # c.pack()

        # frame = Frame(self)
        # frame.grid()
        s = ttk.Style()
        s.theme_use('alt')
        s.configure("blue.Horizontal.TProgressbar", troughcolor='white', background='#F2E500', relief="flat")
        self.progress = ttk.Progressbar(self, style="blue.Horizontal.TProgressbar", orient="horizontal", length=800,
                                        mode="determinate", maximum=200)
        self.progress.place(rely=1.0, relx=1.0, x=-40, y=10, anchor=SE)
        self.progress.pack(side=BOTTOM)
        self.progress['value'] = 0
        # self.progress = ttk.Progressbar(self, orient=HORIZONTAL,
        #                       length=100, mode='determinate')

        # self.progress.place(rely=1.0, relx=1.0, x=200, y=400, anchor=SE)
        # self.progress.pack()

        self.button_start.place(rely=1.0, relx=1.0, x=-20, y=-20, anchor=SE)
        self.screen.pack(side=TOP)
        c = Checkbutton(self, text='Standalone', variable=self.var, onvalue=1, offvalue=0, bg='white').place(rely=1.0,
                                                                                                             relx=1.0,
                                                                                                             x=-568,
                                                                                                             y=-90)

    # -----------------------------------------------------Methods-----------------------------------------------------------------

    def set_standalone(self, var):

        self.standalone = var

    def file_open(self, event=None):
        ini_file = tkf.askopenfilename(filetypes=[("Log File", "*.txt")], initialdir=self.program_location)
        while ini_file and not ini_file.endswith(".txt"):
            msg.showerror("Wrong Filetype", "Please select an txt file")
            ini_file = tkf.askopenfilename()
            if ini_file:
                from os import startfile
                startfile(ini_file)

    def file_add(self, event=None):
        self.xml_file = tkf.askopenfilename(filetypes=[("Xml file", "*.xml")])
        while self.xml_file and not self.xml_file.endswith(".xml"):
            msg.showerror("Wrong Filetype", "Please select an xml file")
            self.xml_file = tkf.askopenfilename()
        # print(self.xml_file)

    def bar(self, val_time=0):
        import time
        if self.progress['value'] == 200:
            self.progress['value'] = 0
        self.progress['value'] = self.progress['value'] + 20 + val_time

        self.update_idletasks()
        time.sleep(1)

    def start_program(self):
        self.folder_path = self.entry_project.get()
        self.spec_name = self.entry_spec.get()
        if (self.folder_path and self.spec_name) or (self.folder_path and self.xml_file) or (
                self.folder_path and len(self.entry_spec.get()) != 0):
            prj_folder_format = self.folder_path
            if not prj_folder_format.endswith(r'work'):
                self.start_program_cond = False
                self.prj_problem()
            elif 'R001' not in self.spec_name:
                self.start_program_cond = False
                self.spec_problem()
            else:
                self.start_program_cond = True
                # print(self.standalone)
                self.standalone = self.var.get()
                # self.log_window()
                base.base_program(self)

        else:
            win = Toplevel()
            win.iconbitmap(
                self.program_location + r"\Interface\top_left.ico")
            win.wm_title("Warning")
            win.geometry('300x100')
            win.configure(background='white')

            l = ttk.Label(win, background='white', text="One or both fields are empty")
            # l.grid(row=0, column=80)
            l.place(rely=1.0, relx=1.0, x=-70, y=-80, anchor=SE)

            b = ttk.Button(win, text="Okay", command=win.destroy, style='Fun.TButton')
            b.place(rely=1.0, relx=1.0, x=-110, y=-20, anchor=SE)

    def finish(self, txt):
        win = Toplevel()
        win.iconbitmap(
            self.program_location + r"\Interface\top_left.ico")
        win.wm_title("Finish")
        win.geometry('400x100')
        win.configure(background='white')

        l = ttk.Label(win, background='white', text=txt)
        # l.grid(row=0, column=80)
        l.pack(side=TOP)

        b = ttk.Button(win, text="Okay", command=win.destroy, style='Fun.TButton')
        b.pack(side=TOP)

    def popup_printinginfo(self):
        win = Toplevel()
        win.iconbitmap(
            self.program_location + r"\Interface\top_left.ico")
        win.wm_title("Warning")
        win.geometry('300x100')
        win.configure(background='white')

        l = ttk.Label(win, background='white', text="One or both fields are empty!")
        # l.grid(row=0, column=80)
        l.place(rely=1.0, relx=1.0, x=-70, y=-80, anchor=SE)

        b = ttk.Button(win, text="Okay", command=win.destroy, style='Fun.TButton')
        b.place(rely=1.0, relx=1.0, x=-110, y=-20, anchor=SE)

    def prj_problem(self):
        win = Toplevel()
        win.iconbitmap(
            self.program_location + r"\Interface\top_left.ico")
        win.wm_title("Warning")
        win.geometry('300x100')
        win.configure(background='white')

        l = ttk.Label(win, background='white',
                      text="Project path must have the following structure:\n d:\\p\\REC01\\rec01_0u0_100\\work  ")
        # l.grid(row=0, column=80)
        l.pack(side=TOP)

        b = ttk.Button(win, text="Okay", command=win.destroy, style='Fun.TButton')
        b.place(rely=1.0, relx=1.0, x=-110, y=-20, anchor=SE)

    def spec_problem(self):
        win = Toplevel()
        win.iconbitmap(
            self.program_location + r"\Interface\top_left.ico")
        win.wm_title("Warning")
        win.geometry('300x100')
        win.configure(background='white')

        l = ttk.Label(win, background='white',
                      text="Spec must include R001 in its name")
        # l.grid(row=0, column=80)
        l.pack(side=TOP)

        b = ttk.Button(win, text="Okay", command=win.destroy, style='Fun.TButton')
        b.place(rely=1.0, relx=1.0, x=-110, y=-20, anchor=SE)

    def use_item(self):
        self.entry_project.delete(0, 'end')
        self.folder_path = ''
        if not self.folder_path:
            self.folder_path = tkf.askdirectory()
            self.entry_project.insert(0, self.folder_path)
        # print(self.folder_path)

    '''
    def console_log(self, txt):
        win = Toplevel()
        win.wm_title("Warning")
        win.geometry('800x800')
        win.configure(background='white')
        e = Text(win)
        e.pack(side=TOP)
        sys.stdout = win
        self.write(txt, e)
    '''

    # win.doIt = Button(self, text="DoIt", command=self.onEnter)
    # self.doIt.pack()
    # output = Text()
    # output.pack()
    # output.insert(END, str(txt))
    # sys.stdout = win
    # win.pack()

    def value_get(self):
        self.spec_name = self.entry_spec.get()
        # print(self.entry_spec.get())

    def set_screen(self, screens):
        self.screens = screens

    def display_screen(self):
        self.active_screen = self.screens
        self.screen.delete("all")
        self.screen.create_image((390, 200), image=self.active_screen.image)

    def start(self):
        if not self.screens:
            print("No screens added!")
        else:
            self.display_screen()

    def browse_button_project(self):
        filename = tkf.askdirectory()
        folder_path = filename
        self.canvas.create_window(200, 30, window=self.entry1)
        self.entry1.insert(2, folder_path)

    def get_prj_loc(self):
        try:
            return self.entry_project()
        except Exception as e:
            print(e)

    def get_spec_name(self):
        try:
            return self.entry_spec.get()
        except Exception as e:
            print(e)


'''
    def log_window(self):
        self = ttk.Style()
        self.theme_use('clam')

        t = Toplevel(self)
        t.wm_title("Window Log %s")
        t.pack()
'''

if __name__ == '__main__':
    # print(os.path.dirname(os.path.abspath(__file__)))
    app = App()
    a1 = AppScreen(app,
                   r'Interface\bg2.png')
    app.set_screen(a1)
    app.start()
    app.mainloop()
