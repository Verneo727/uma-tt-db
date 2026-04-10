#!/usr/bin/env python3

"""Help window"""

import tkinter as tk
from PIL import Image, ImageTk

from core.i18n import I18n
from setup.resources import resource_path

class Help(tk.Toplevel):
    def __init__(self, lang, master=None):
        super().__init__(master=master)
        self.master = master
        self.lang = lang
        self.i18n = I18n(language=self.lang)
        self.title(f"{self.i18n.t("help.title")}")
        self.geometry("600x800")

        self._qui()

    def _qui(self):
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.page_classes = [StartPage, AddUma, SetTeam, AddTrial]
        self.frames = {}
        self.current_index = 0

        for F in self.page_classes:
            page_name = F.__name__
            frame = F(parent=container, controller=self, i18n=self.i18n)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        nav_bar = tk.Frame(self)
        nav_bar.pack(side="bottom", fill="x", pady=10)

        self.btn_prev = tk.Button(
            nav_bar, 
            text=f"< {self.i18n.t("help.previous")}", 
            command=self.go_prev,
            )
        self.btn_prev.pack(side="left", padx=20)

        self.btn_next = tk.Button(
            nav_bar,
            text=f"{self.i18n.t("help.next")} >",
            command=self.go_next,
            )
        self.btn_next.pack(side="right", padx=20)

        self.show_page()

    def show_page(self):
        page_class = self.page_classes[self.current_index]
        page_name = page_class.__name__
        frame = self.frames[page_name]
        frame.tkraise()

        self.btn_prev.config(state="normal" if self.current_index > 0 else "disabled")
        self.btn_next.config(state="normal" if self.current_index < len(self.page_classes) - 1 else "disabled")

    def go_next(self):
        if self.current_index < len(self.page_classes) - 1:
            self.current_index += 1
            self.show_page()

    def go_prev(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_page()

class StartPage(tk.Frame):
    def __init__(self, parent, controller, i18n):
        super().__init__(parent)
        self.controller = controller
        self.i18n = i18n

        label = tk.Label(
            self,
            text=f"{self.i18n.t("help.title").upper()}",
            font=("Arial", 18, "bold"))
        label.pack(pady=50)
        tk.Label(self, text=f"{self.i18n.t("help.welcome")}").pack()
        next = tk.Label(self, text=f"{self.i18n.t("help.welcome2")}")
        next.config(font=("TkDefaultFont", 10, "bold"))
        next.pack(pady=25)

        # ! Refactor as it expands:
        tk.Label(
            self,
            text=f"{self.i18n.t("help.authors")}"
            ).pack(pady=60)

class AddUma(tk.Frame):
    def __init__(self, parent, controller, i18n):
        super().__init__(parent)
        self.controller = controller
        self.i18n = i18n

        tk.Label(self,
                 text=f"{self.i18n.t("help.adding_uma")}",
                 font=("Arial", 18, "bold")
                 ).pack(pady=50)
        tk.Label(self, text=f"{self.i18n.t("help.first")}").pack(pady=20)
        tk.Label(self, text=f"{self.i18n.t("help.first2")}").pack()
        tk.Label(self, text=f"{self.i18n.t("help.first3")}").pack()
        adduma_file = resource_path(f'uma-tt-db/assets/img/add_uma.png')
        adduma_img = Image.open(str(adduma_file))
        self.add_uma_img = ImageTk.PhotoImage(adduma_img)
        add_uma = tk.Label(self, image=self.add_uma_img)
        add_uma.pack(pady=10)
        tk.Label(self, text=f"{self.i18n.t("help.first4")}").pack(pady=7)
        tk.Label(self, text=f"{self.i18n.t("help.first5")}").pack()

class SetTeam(tk.Frame):
    def __init__(self, parent, controller, i18n):
        super().__init__(parent)
        self.controller = controller
        self.i18n = i18n

        tk.Label(self,
                 text=f"{self.i18n.t("help.set_team")}",
                 font=("Arial", 18, "bold")
                 ).pack(pady=50)
        tk.Label(self, text=f"{self.i18n.t("help.set1")}").pack(pady=20)
        tk.Label(self, text=f"{self.i18n.t("help.set2")}").pack()
        tk.Label(self, text=f"{self.i18n.t("help.set3")}").pack()
        setsquad_file = resource_path(f'uma-tt-db/assets/img/set_squad.png')
        squad_img = Image.open(str(setsquad_file))
        new_size = (320, 320)
        squad_img = squad_img.resize(new_size, Image.LANCZOS)
        self.set_squad_img = ImageTk.PhotoImage(squad_img)
        set_squad = tk.Label(self, image=self.set_squad_img)
        set_squad.pack(pady=10)
        tk.Label(self, text=f"{self.i18n.t("help.set4")}").pack(pady=7)
        tk.Label(self, text=f"{self.i18n.t("help.set5")}").pack()

class AddTrial(tk.Frame):
    def __init__(self, parent, controller, i18n):
        super().__init__(parent)
        self.controller = controller
        self.i18n = i18n

        tk.Label(self,
                 text=f"{self.i18n.t("help.add_trial")}",
                 font=("Arial", 18, "bold")
                 ).pack(pady=50)
        tk.Label(self, text=f"{self.i18n.t("help.trial1")}").pack(pady=20)
        tk.Label(self, text=f"{self.i18n.t("help.trial2")}").pack()
        tk.Label(self, text=f"{self.i18n.t("help.trial3")}").pack()
        tk.Label(self, text=f"{self.i18n.t("help.trial4")}").pack()
        tk.Label(self, text=f"{self.i18n.t("help.trial5")}").pack()
        add_tt_file = resource_path(f'uma-tt-db/assets/img/add_tt.png')
        add_tt_img = Image.open(str(add_tt_file))
        self.add_tt_img = ImageTk.PhotoImage(add_tt_img)
        add_tt = tk.Label(self, image=self.add_tt_img)
        add_tt.pack(pady=10)
        tk.Label(self, text=f"{self.i18n.t("help.trial6")}").pack()