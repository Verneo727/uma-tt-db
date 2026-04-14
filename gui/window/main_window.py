#!/usr/bin/env python3

import tkinter as tk
import webbrowser
import random

from core.i18n import I18n
from core.tooltip import ToolTip
from core.close import close
from database.db_manager import pragma
from gui.window.lang import ask_lang

from metadata import __author__, __version__
from assets.random_texts import RANDOM_TEXT

class MainWindow(tk.Toplevel):
    def __init__(self, app_path, lang, __app_name__, master=None):
        super().__init__(master)
        self.master = master
        self.title(__app_name__)
        self.geometry('600x630')

        self.app_path = app_path
        self.lang = lang
        self.i18n = I18n(language=lang)

        #self.icon = tk.PhotoImage(file=f'{BASE}/assets/icons/carats.png')
        #self.iconphoto(True, self.icon)
        self._qui()

    def _qui(self):
        # LOGO
        # Due to the lack of suitable CC0-licensed graphics,
        # I cannot place anything in this section.
        # If you would like to help by creating your own image,
        # please contact the program's author.
        logo = tk.Label(
            self,
            text=f"{self.i18n.t("main_menu.info")}",
            fg="gray")
        logo.pack(side="top", anchor="n", pady=10)

        # DATABASE PRAGMA
        version = pragma(self.app_path)
        pragma_text = f"{self.i18n.t("main_menu.pragma")} {version}"
        pragma_label = tk.Label(self, text=pragma_text, fg="gray")
        ToolTip(pragma_label, f"{self.i18n.t("main_menu.pragma_info")}")
        pragma_label.pack(side="top", anchor="nw", padx=10, pady=40)

        # GOLD RANDOM TEXT
        parent_bg = self.master.cget('bg') if hasattr(self, 'master') and self.master else "#d9d9d9"
        self.splash_canvas = tk.Canvas(self, bg=parent_bg, highlightthickness=0,
                                      width=400, height=50)
        self.splash_canvas.pack(anchor="e", pady=5)
        # You can add more random text in assets/random_texts.py
        text = random.choice(RANDOM_TEXT)
        self._draw_outlined_text(self.splash_canvas, 350, 25, text)

        # ADD NEW UMA
        add_uma_button = tk.Button(
            self,
            text=f"{self.i18n.t("main_menu.add_uma")}",
            relief="solid",
            borderwidth=1,
            command=lambda: self._add_uma(lang=self.lang),
        )
        add_uma_button.config(width=20)
        ToolTip(add_uma_button, f"{self.i18n.t("main_menu.add_uma_info")}")
        add_uma_button.pack()

        # ADD TRIAL RUN
        add_trial_run_button = tk.Button(
            self,
            text=f"{self.i18n.t("main_menu.add_trial")}",
            relief="solid",
            borderwidth=1,
            command=lambda: self._add_trial(self.app_path),
        )
        add_trial_run_button.config(width=20)
        ToolTip(add_trial_run_button, f"{self.i18n.t("main_menu.add_trial_info")}")
        add_trial_run_button.pack()

        # ADD RESULTS
        add_results_button = tk.Button(
            self,
            text=f"{self.i18n.t("main_menu.add_results")}",
            relief="solid",
            borderwidth=2,
            command=lambda: self._add_results(self.app_path),
        )
        add_results_button.config(width=20)
        ToolTip(add_results_button, f"{self.i18n.t("main_menu.add_results_info")}")
        add_results_button.pack()

        # SHOW RESULTS WINDOW
        show_results_window = tk.Button(
            self,
            text=f"{self.i18n.t("main_menu.show_results")}",
            relief="solid",
            borderwidth=1,
            command=lambda: self._show_results(self.app_path),
        )
        show_results_window.config(width=20, cursor="hand2")
        ToolTip(show_results_window, f"{self.i18n.t("main_menu.show_results_info")}")
        show_results_window.pack()

        # SET ACTUAL TEAM
        actual_team_button = tk.Button(
            self,
            text=f"{self.i18n.t("main_menu.choose_team")}",
            relief="solid",
            borderwidth=1,
            command=lambda: self._set_actual_team(self.app_path, lang=self.lang),
        )
        actual_team_button.config(width=20, cursor="hand2")
        ToolTip(actual_team_button, f"{self.i18n.t("main_menu.choose_team_info")}")
        actual_team_button.pack(pady=20)

        # HELP and LANGUAGE ROW
        help_row = tk.Frame(self)
        help_row.pack(fill="x", pady=20)

        help_row.columnconfigure(0, weight=1, uniform="group1")
        help_row.columnconfigure(1, weight=0)
        help_row.columnconfigure(2, weight=1, uniform="group1")

        # LANG WINDOW
        lang_button = tk.Button(
            help_row,
            text="🌐",
            font=("Arial", 16),
            relief="solid",
            borderwidth=1,
            command=lambda: self._language(self.app_path),
        )
        ToolTip(lang_button, f"{self.i18n.t("main_menu.lang_info")}")
        lang_button.grid(row=0, column=0, sticky="e", padx=10)

        # HELP WINDOW
        help_button = tk.Button(
            help_row,
            text=f"{self.i18n.t("main_menu.help")}",
            relief="raised",
            borderwidth=1,
            command=lambda: self._help(lang=self.lang),
        )
        help_button.config(width=20, cursor="hand2")
        ToolTip(help_button, f"{self.i18n.t("main_menu.help_info")}")
        help_button.grid(row=0, column=1)

        # BOTTOM INFO LABEL
        info_label = tk.Label(
            self,
            relief="solid",
            borderwidth=1,
            bg="snow")
        info_label.pack(fill="x", side="bottom", anchor="sw")

        author_lbl = tk.Label(
            info_label,
            text=f"{self.i18n.t("main_menu.author")}: {__author__}",
            anchor="w",
            bg="snow",
        )
        author_lbl.pack(side="left", padx=5)

        version_lbl = tk.Label(
            info_label,
            text=f"{self.i18n.t("main_menu.version")}: {__version__}",
            anchor="w",
            bg="snow",
        )
        version_lbl.pack(side="left", padx=5)

        html_license = "http://www.gnu.org/licenses/"
        license_lbl = tk.Label(
            info_label,
            text="GNU GPL v3.0",
            anchor="w",
            bg="snow",
            cursor="hand2",
        )
        ToolTip(license_lbl, f"{self.i18n.t("main_menu.license_info")}")
        license_lbl.bind("<Button-1>", lambda event: self._open_url(html_license))
        license_lbl.pack(side="left", padx=5)

        github_url = "https://github.com/jamrozmat/uma-tt-db"
        github_lbl = tk.Label(
            info_label,
            text="uma-tt-db Github",
            relief="groove",
            borderwidth=1,
            anchor="w",
            bg="gainsboro",
            cursor="hand2",
        )
        ToolTip(github_lbl, f"{self.i18n.t("main_menu.github_info")}")
        github_lbl.bind("<Button-1>", lambda event: self._open_url(github_url))
        github_lbl.pack(side="right")

        exit_btn = tk.Button(
            self,
            text=f"{self.i18n.t("main_menu.exit")}",
            relief="solid",
            borderwidth=1,
            command=self._close_program,
        )
        exit_btn.config(width=20)
        exit_btn.pack(side="bottom", pady=5)
        ToolTip(exit_btn, f"{self.i18n.t("main_menu.exit_info")}")

    def _add_uma(self, lang):
        from gui.window.add_uma import AddUma
        uma_window = AddUma(master=self, lang=self.lang, app_path=self.app_path)
        uma_window.focus_set()
        uma_window.grab_set()

    def _add_trial(self, app_path):
        from gui.window.add_trial import AddTrial
        trial_window = AddTrial(master=self, app_path=app_path, lang=self.lang)
        trial_window.focus_set()
        trial_window.grab_set()

    def _add_results(self, app_path):
        from gui.window.add_results import AddResults
        result_window = AddResults(master=self, app_path=app_path, lang=self.lang)
        result_window.focus_set()
        result_window.grab_set()

    def _show_results(self, app_path):
        from gui.window.show_results import ShowResults
        show_results_window = ShowResults(master=self, app_path=app_path, lang=self.lang)
        show_results_window.focus_set()
        show_results_window.grab_set()

    def _set_actual_team(self, app_path, lang):
        from gui.window.set_team import ActualTeam
        set_team_window = ActualTeam(master=self, app_path=app_path, lang=self.lang)
        set_team_window.focus_set()
        set_team_window.grab_set()

    def _help(self, lang):
        from gui.window.help import Help
        help_window = Help(master=self, lang=self.lang)
        help_window.focus_set()
        help_window.grab_set()

    def _language(self, app_path):
        lang_window = ask_lang(app_path)
        lang_window.focus_set()
        lang_window.grab_set()

    def _open_url(self, html):
        webbrowser.open(html)

    def _close_program(self):
        close()

    def _draw_outlined_text(self, canvas, x, y, text_content, main_color="gold", outline_color="black"):
        text_font = ("Helvetica", 12, "bold")
        offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in offsets:
            canvas.create_text(x + dx, y + dy, text=text_content, fill=outline_color,
                            font=text_font, anchor="e")

        return canvas.create_text(x, y, text=text_content, fill=main_color,
                                font=text_font, anchor="e")