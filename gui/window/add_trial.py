#!/usr/bin/env python3

import tkinter as tk
import datetime as dt
from tkinter import messagebox

from core.tooltip import ToolTip
from core.i18n import I18n
from database.add_trial import add_trial_to_db
from setup.config_vals import remember_date_load
from setup.config_vals import trial_autoload


class AddTrial(tk.Toplevel):
    def __init__(self, app_path, lang, master=None):
        super().__init__(master=master)
        self.master = master
        self.app_path = app_path
        self.i18n = I18n(language=lang)
        self.title(f"{self.i18n.t("add_trial.title")}")
        self.geometry("280x220")
        self.resizable(width=False, height=False)

        self.remember_date_val = tk.BooleanVar(value=remember_date_load(self.app_path))

        self._gui()

    def _gui(self):
        info_text = f"{self.i18n.t("add_trial.info")}"
        self.info_label = tk.Label(
            self,
            text=info_text,
            font=("Helvetica", 10, "italic"),
            anchor="n",
        )
        self.info_label.config(padx=10, pady=10)
        self.info_label.grid(sticky="n")

        self.entries_frame = tk.Frame(self, padx=10, pady=10)
        self.entries_frame.grid()

        self.date_text_label = tk.Label(
            self.entries_frame,
            text=f"{self.i18n.t("add_trial.date")}: ",
            font=("Helvetica", 10),
        )
        ToolTip(self.date_text_label, f"{self.i18n.t("add_trial.date_info")}")
        self.date_text_label.grid(row=0, column=0, sticky="w")

        self.date_today_btn = tk.Button(
            self.entries_frame,
            text="T",
            relief="solid",
            borderwidth=1,
            width=1,
            height=1,
            command=self._add_date,
        )
        ToolTip(self.date_today_btn, f"{self.i18n.t("add_trial.today")}")
        self.date_today_btn.grid(row=0, column=1)

        self.date_var = tk.StringVar()
        self.trace_date = self.date_var.trace_add("write", self._format_date)
        self.date_entry = tk.Entry(
            self.entries_frame,
            textvariable=self.date_var,
            justify="left",
            width=10,
        )
        self.date_entry.grid(row=0, column=2, sticky="w")

        self.hour_text_label = tk.Label(
            self.entries_frame,
            text=f"{self.i18n.t("add_trial.hour")}: ",
            font=("Helvetica", 10),
        )
        ToolTip(self.hour_text_label, f"{self.i18n.t("add_trial.hour_info")}")
        self.hour_text_label.grid(row=1, column=0, sticky="w", pady=2)

        self.time_var = tk.StringVar()
        self.trace_time = self.time_var.trace_add("write", self._format_time)
        self.hour_entry = tk.Entry(
            self.entries_frame,
            textvariable=self.time_var,
            justify="left",
            width=10,
        )
        self.hour_entry.grid(row=1, column=2, sticky="w", pady=2)

        self.save_check = tk.Checkbutton(
            self,
            text=f"{self.i18n.t("add_trial.check")}",
            font=("Helvetica", 10),
            command=lambda: self._saving_check(self.remember_date_val),
            variable=self.remember_date_val,
        )
        ToolTip(self.save_check, f"{self.i18n.t("add_trial.check_info")}")
        self.save_check.grid(padx=10, pady=2)

        self.btn_row = tk.Frame(self)
        self.btn_row.grid(padx=10, pady=15)

        self.exit_btn = tk.Button(
            self.btn_row,
            text=f"{self.i18n.t("add_trial.exit")}",
            font=("Helvetica", 10),
            relief="solid",
            borderwidth=1,
            command=lambda: self._quit(),
        )
        self.exit_btn.grid(row=0, column=0, padx=5)

        self.add_trial_btn = tk.Button(
            self.btn_row,
            text=f"{self.i18n.t("add_trial.add_trial_btn")}",
            font=("Helvetica", 10),
            relief="solid",
            borderwidth=2,
            command=self._add_trial,
        )
        self.bind("<Return>", self._add_trial)  # Enter for all this window
        self.add_trial_btn.grid(row=0, column=1, padx=5)

        self.btn_row.columnconfigure(0, weight=1)
        self.btn_row.columnconfigure(1, weight=1)

    def _add_trial(self, event=None):
        date = self.date_entry.get()
        hour = self.hour_entry.get()

        if not date or not hour:
            messagebox.showwarning("Error!", "Wypełnij wszystkie pola!")
            return

        success, error = add_trial_to_db(date, hour)
        if not success:
            messagebox.showerror("Database Error", f"{error}")
        else:
            pass

        self.hour_entry.delete(0, tk.END)
        self.hour_entry.icursor(0)
        self.hour_entry.focus_set()
        if self.remember_date_val.get() is not True:
            self.date_entry.delete(0, tk.END)
            self.date_entry.focus_set()

    def _add_date(self):
        today = dt.datetime.strftime('%Y-%m-%d')
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, today)

    def _format_time(self, *args):
        text = self.time_var.get()
        digits = "".join([char for char in text if char.isdigit()])
        digits = digits[:6]
        formatted = ""
        for i, char in enumerate(digits):
            if i == 2 or i == 4:
                formatted += ":"
            formatted += char

        self.time_var.trace_remove("write", self.trace_time)
        self.time_var.set(formatted)
        self.hour_entry.after(10, lambda: self.hour_entry.icursor(tk.END))
        self.trace_time = self.time_var.trace_add("write", self._format_time)

    def _format_date(self, *args):
        text = self.date_var.get()
        digits = "".join([char for char in text if char.isdigit()])
        digits = digits[:8]
        formatted = ""
        for i, char in enumerate(digits):
            if i == 4 or i == 6:
                formatted += "-"
            formatted += char

        self.date_var.trace_remove("write", self.trace_date)
        self.date_var.set(formatted)
        self.date_entry.after(10, lambda: self.date_entry.icursor(tk.END))
        self.trace_date = self.date_var.trace_add("write", self._format_date)

    def _saving_check(self, remember_date_val):
        check_val = remember_date_val.get()
        if check_val is True:
            trial_autoload(self.app_path, check_val)
        else:
            trial_autoload(self.app_path, check_val)

    def _quit(self):
        self.destroy()