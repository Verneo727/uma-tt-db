#!/usr/bin/env python3

import tkinter as tk
import datetime as dt
from tkinter import messagebox
from tkinter import ttk

from core.tooltip import ToolTip
from core.i18n import I18n
from database.add_trial import add_trial_to_db
from database.get_trials import load_class
from database.get_trials import load_difficulty
from database.get_rivals import search_rivals
from setup.config_vals import remember_date_load
from setup.config_vals import load_hour_format
from setup.config_vals import trial_autoload
from setup.config_vals import save_hour_format


class AddTrial(tk.Toplevel):
    def __init__(self, app_path, lang, master=None):
        super().__init__(master=master)
        self.master = master
        self.app_path = app_path
        self.i18n = I18n(language=lang)
        self.title(f"{self.i18n.t("add_trial.title")}")
        self.geometry("310x420")
        self.resizable(width=False, height=False)

        self.remember_date_val = tk.BooleanVar(value=remember_date_load(self.app_path))
        self.is_24h = load_hour_format(self.app_path)
        self.class_values = load_class(self.app_path)
        self.class_map = {name: class_id for class_id, name in self.class_values}
        self.diff_values = load_difficulty(self.app_path)
        self.diff_map = {name: diff_id for diff_id, name in self.diff_values}
        self.current_suggestion = ""

        self._gui()

    def _gui(self):
        self._info()
        self._required_entries()
        self._optional_entries()
        self._buttons()

    def _info(self):
        info_text = f"{self.i18n.t("add_trial.info")}"
        self.info_label = tk.Label(
            self,
            text=info_text,
            font=("Helvetica", 10, "italic"),
            anchor="n",
        )
        self.info_label.config(padx=10, pady=10)
        self.info_label.grid(sticky="new")

        self.saved_label = tk.Label(
            self,
            text="",
            font=("Helvetica", 10, "bold italic"),
            bg=self.cget("bg"),
        )
        self.saved_label.config(padx=10, pady=2)
        self.saved_label.grid(sticky="ew")

    def _required_entries(self):
        self.entries_frame = tk.LabelFrame(self,
                                           text=self.i18n.t("add_trial.required"),
                                           font=("Helvetica", 10, "bold"),
                                           padx=10, pady=10)
        self.entries_frame.grid(padx=(5, 5), pady=5, sticky="ew")

        self.date_text_label = tk.Label(
            self.entries_frame,
            text=f"{self.i18n.t("add_trial.date")}: ",
            font=("Helvetica", 10),
        )
        ToolTip(self.date_text_label, f"{self.i18n.t("add_trial.date_info")}")
        self.date_text_label.grid(row=0, column=0, sticky="w")

        self.date_today_btn = tk.Button(
            self.entries_frame,
            text=f"{self.i18n.t("add_trial.today_btn")}",
            relief="solid",
            borderwidth=1,
            width=5,
            height=1,
            command=self._add_date,
        )
        ToolTip(self.date_today_btn, f"{self.i18n.t("add_trial.today")}")
        self.date_today_btn.grid(row=0, column=1, sticky="ew")

        self.date_var = tk.StringVar()
        self.trace_date = self.date_var.trace_add("write", self._format_date)
        self.date_entry = tk.Entry(
            self.entries_frame,
            textvariable=self.date_var,
            justify="left",
            width=10,
        )
        self.date_entry.grid(row=0, column=2, sticky="ew")

        self.hour_text_label = tk.Label(
            self.entries_frame,
            text=f"{self.i18n.t("add_trial.hour")}: ",
            font=("Helvetica", 10),
        )
        ToolTip(self.hour_text_label, f"{self.i18n.t("add_trial.hour_info")}")
        self.hour_text_label.grid(row=1, column=0, sticky="w", pady=2)

        self.hour_format_btn = tk.Button(
            self.entries_frame,
            text="24H" if self.is_24h else "AM/PM",
            relief="solid",
            borderwidth=1,
            width=5,
            height=1,
            command=self._toggle_time_format,
        )
        ToolTip(self.hour_format_btn, f"{self.i18n.t("add_trial.hour_format_btn")}")
        self.hour_format_btn.grid(row=1, column=1)

        self.time_var = tk.StringVar()
        self.trace_time = self.time_var.trace_add("write", self._format_time)
        self.hour_entry = tk.Entry(
            self.entries_frame,
            textvariable=self.time_var,
            justify="left",
            width=10,
        )
        self.hour_entry.grid(row=1, column=2, sticky="ew", pady=2)

        self.save_check = tk.Checkbutton(
            self,
            text=f"{self.i18n.t("add_trial.check")}",
            font=("Helvetica", 10),
            command=lambda: self._saving_check(self.remember_date_val),
            variable=self.remember_date_val,
        )
        ToolTip(self.save_check, f"{self.i18n.t("add_trial.check_info")}")
        self.save_check.grid(padx=10, pady=2)

    def _optional_entries(self):
        self.optional_opts_frame = tk.LabelFrame(self,
                                                 text=self.i18n.t("add_trial.optional"),
                                                 font=("Helvetica", 10, "bold"),
                                                 padx=10, pady=10,)
        self.optional_opts_frame.grid(padx=(5, 5), pady=(20, 0), sticky="ew")

        self.optional_opts_frame.columnconfigure(0, weight=1)
        self.optional_opts_frame.columnconfigure(1, weight=1)

        self.points_lbl = tk.Label(
            self.optional_opts_frame,
            text=f"{self.i18n.t("add_trial.points")}:",
            font=("Helvetica", 10,),
        )
        self.points_lbl.grid(row=0, column=0, sticky="w", pady=(0, 2))

        self.points_entry = tk.Entry(self.optional_opts_frame, width=10)
        self.points_entry.grid(row=0, column=1, sticky="ew", pady=(0, 2))

        self.rival_lbl = tk.Label(
            self.optional_opts_frame,
            text=f"{self.i18n.t("add_trial.rival")}:",
            font=("Helvetica", 10),
        )
        self.rival_lbl.grid(row=1, column=0, sticky="w")

        self.rival_entry = tk.Entry(self.optional_opts_frame, width=10)
        self.rival_entry.grid(row=1, column=1, sticky="ew")
        self.rival_entry.bind("<KeyRelease>", self._on_rival_typing)
        self.rival_entry.bind("<Tab>", self._on_rival_tab)

        self.rival_suggestion_lbl = tk.Label(
            self.optional_opts_frame,
            text="...",
            fg="gray",
            font=("Helvetica", 10)
        )
        self.rival_suggestion_lbl.grid(row=2, column=1, sticky="w", pady=(0, 2))

        self.class_diff_frame = tk.Frame(self.optional_opts_frame)
        self.class_diff_frame.grid(row=3, columnspan=2, sticky="ew", pady=(2, 0))
        self.class_diff_frame.columnconfigure(0, weight=1)
        self.class_diff_frame.columnconfigure(1, weight=1)
        self.class_diff_frame.columnconfigure(2, weight=1)
        self.class_diff_frame.columnconfigure(3, weight=1)

        self.class_lbl = tk.Label(
            self.class_diff_frame,
            text=self.i18n.t("add_trial.class") + ":",
            font=("Helvetica", 10),
        )
        self.class_lbl.grid(row=0, column=0, sticky="w")

        self.class_combo = ttk.Combobox(
            self.class_diff_frame,
            values=list(self.class_map.keys()),
            state="readonly",
            width=5)
        self.class_combo.grid(row=0, column=1)

        self.difficulty_lbl = tk.Label(
            self.class_diff_frame,
            text=self.i18n.t("add_trial.diff") + ":",
            font=("Helvetica", 10),
        )
        self.difficulty_lbl.grid(row=0, column=2, sticky="w")

        self.difficulty_combo = ttk.Combobox(
            self.class_diff_frame,
            values=list(self.diff_map.keys()),
            state="readonly",
            width=5)
        self.difficulty_combo.grid(row=0, column=3)

    def _buttons(self):
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

    def _toggle_time_format(self):
        current_val = self.time_var.get().strip()
        if not current_val:
            self.is_24h = not self.is_24h
            self.hour_format_btn.config(text="24H" if self.is_24h else "AM/PM")
            save_hour_format(self.is_24h, self.app_path)
            return

        try:
            if self.is_24h:
                time_set = dt.datetime.strptime(current_val, "%H:%M:%S")
                new_time = time_set.strftime("%I:%M:%S %p")
                self.is_24h = False
                self.hour_format_btn.config(text="AM/PM")
            else:
                time_set = dt.datetime.strptime(current_val, "%I:%M:%S %p")
                new_time = time_set.strftime("%H:%M:%S")
                self.is_24h = True
                self.hour_format_btn.config(text="24H")

            self.time_var.trace_remove("write", self.trace_time)
            self.time_var.set(new_time)
            self.trace_time = self.time_var.trace_add("write", self._format_time)
        except ValueError:
            self.is_24h = not self.is_24h
            self.hour_format_btn.config(text="24H" if self.is_24h else "AM/PM")

        save_hour_format(self.is_24h, self.app_path)

    def _add_trial(self, event=None):
        date = self.date_entry.get().strip()
        hour = self.hour_entry.get().strip()

        score = self.points_entry.get().strip()
        score = int(score) if score else None

        nick = self.rival_entry.get().strip()
        nick = nick if nick else None

        selected_class = self.class_combo.get()
        class_id = self.class_map.get(selected_class) if selected_class else None

        selected_diff = self.difficulty_combo.get()
        diff_id = self.diff_map.get(selected_diff) if selected_diff else None

        if not date or not hour:
            messagebox.showwarning(f"{self.i18n.t("m_b.error")}!", f"{self.i18n.t("m_b.all_entries")}!")
            return

        try:
            if not self.is_24h:
                time_obj = dt.datetime.strptime(hour, "%I:%M:%S %p")
            else:
                time_obj = dt.datetime.strptime(hour, "%H:%M:%S")

            hour_to_save = time_obj.strftime("%H:%M:%S")

        except ValueError:
            messagebox.showerror(f"{self.i18n.t("m_b.format_error")}",
                f"{self.i18n.t("m_b.incorrect_hour_format")}!")
            return

        success, error = add_trial_to_db(
            date, hour_to_save, self.app_path,
            score, nick, class_id, diff_id
            )
        if not success:
            messagebox.showerror(f"{self.i18n.t("m_b.db_error")}", f"{error}")
        else:
            self.time_var.trace_remove("write", self.trace_time)
            self.saved_label.config(
                text="✔ " + self.i18n.t("add_trial.saved"),
                fg="black",
                bg="lightgreen",
                )
            self.points_entry.delete(0, tk.END)
            self.rival_entry.delete(0, tk.END)
            self.hour_entry.delete(0, tk.END)
            self.hour_entry.icursor(0)
            if self.remember_date_val.get() is not True:
                self.date_entry.delete(0, tk.END)
                self.date_entry.focus_set()
            else:
                self.hour_entry.focus_set()
            self.trace_time = self.time_var.trace_add("write", self._format_time)

    def _add_date(self):
        today = dt.datetime.now().isoformat()
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, today)

    def _format_time(self, *args):
        self._clear_saved_status()
        text = self.time_var.get().upper()
        digits = "".join([char for char in text if char.isdigit()])[:6]
        suffix = ""
        if hasattr(self, 'is_24h') and not self.is_24h:
            if "P" in text:
                suffix = " PM"
            else:
                suffix = " AM"

        formatted = ""
        for i, char in enumerate(digits):
            if i == 2 or i == 4:
                formatted += ":"
            formatted += char

        full_text = formatted + suffix

        self.time_var.trace_remove("write", self.trace_time)
        self.time_var.set(full_text)
        self.hour_entry.after(10, lambda: self.hour_entry.icursor(len(formatted)))
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

    def _on_rival_typing(self, event):
        if event.keysym in ("BackSpace", "Tab", "Shift_L", "Control_L", "Alt_L"):
            return

        text = self.rival_entry.get()

        if len(text) < 2:
            self.rival_suggestion_lbl.config(text="...")

        elif len(text) >= 2:
            suggestion = search_rivals(self.app_path, text)
            if suggestion:
                self.current_suggestion = suggestion
                self.rival_suggestion_lbl.config(text=f"TAB: {suggestion}" if suggestion else "")
            else:
                self.current_suggestion = ""

    def _on_rival_tab(self, event):
        if self.current_suggestion:
            self.rival_entry.delete(0, tk.END)
            self.rival_entry.insert(0, self.current_suggestion)
            self.current_suggestion = ""
            self.rival_suggestion_lbl.config(text="...")
            return "break"

    def _clear_saved_status(self):
        self.saved_label.config(text="", bg=self.cget("bg"), fg="black")

    def _saving_check(self, remember_date_val):
        check_val = remember_date_val.get()
        if check_val is True:
            trial_autoload(self.app_path, check_val)
        else:
            trial_autoload(self.app_path, check_val)

    def _quit(self):
        self.destroy()