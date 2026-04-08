#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox

from gui.widgets.chart import Chart
from database.get_uma import (
    load_uma_position,
    load_uma_name,
    load_umas_by_distance,
    load_umas_by_trial)
from database.get_team import load_team
from core.i18n import I18n
import numpy as np

class ShowResults(tk.Toplevel):
    def __init__(self, app_path, lang, master=None):
        super().__init__(master = master)
        self.master = master
        self.app_path = app_path
        self.lang = lang
        self.i18n = I18n(language=lang)
        self.title(f"{self.i18n.t("score_win.title")}")
        self.geometry("1000x800")

        self.uma_id = None
        self.runtype_id = None
        self.selected_trials = None

        self.act_sq = tk.BooleanVar(value=False)
        self.json_squad = load_team(app_path)

        self.chart = Chart(self, [], {}, view_size=20)

        self._gui()
        self.refresh_uma_list()
        
    def _gui(self):

        self.list_row = tk.Frame(self)
        self.list_row.pack(side="top", fill='x', padx=10, pady=10)
        self.list_row.columnconfigure(0, weight=1)
        self.list_row.columnconfigure(1, weight=1)
        self.list_row.columnconfigure(2, weight=1)

        uma_list_frame = tk.Frame(self.list_row)
        uma_list_frame.grid(row=0, column=0, sticky="nw")

        self.uma_list_title = tk.Label(
            uma_list_frame, 
            text=f"{self.i18n.t("score_win.uma_list")}:",
            font=("Helvetica", 10, "bold")
            )
        self.uma_list_title.pack(anchor="w")
        
        self.uma_list = tk.Listbox(uma_list_frame,
                                height=10,
                                width=30,
                                bg="grey",
                                activestyle="dotbox",
                                font="Helvetica",
                                )
        self.uma_list.pack(anchor="w")
        self.uma_list.bind("<ButtonRelease-1>", self.on_uma_click)

        self.refresh_uma_list()

        type_run_frame = tk.Frame(self.list_row)
        type_run_frame.grid(row=0, column=1, sticky="n")

        self.type_run_title = tk.Label(
            type_run_frame,
            text=f"{self.i18n.t("score_win.rodzaje")}:",
            font=("Helvetica", 10)
        )
        self.type_run_title.pack(anchor="w")

        self.type_run = tk.Listbox(
            type_run_frame,
            height=5,
            width=30,
            activestyle="dotbox",
            font="Helvetica",
        )
        self.type_run.pack(anchor="w")
        self.type_run.bind("<ButtonRelease-1>", self.on_runtype_click)

        self.is_clicked = tk.Label(
            type_run_frame,
            text=f"{self.i18n.t("score_win.choose")}",
            width=30,
            font=("Helvetica", 10),
            relief="solid",
            borderwidth=1,
            background="#2a2a2a",
            fg="white"
        )
        self.is_clicked.pack(pady=5)

        self.actual_squad = tk.Checkbutton(
            type_run_frame,
            text=f"{self.i18n.t("score_win.dotyczy")}",
            width=30,
            font=("Helvetica", 10),
            command=lambda: self._show_with_act_sq(self.act_sq, uma_ids=None),
            variable=self.act_sq,
        )
        self.actual_squad.pack(pady=2)

        self.close_this = tk.Button(
            type_run_frame,
            text=f"{self.i18n.t("score_win.back")}",
            relief="solid",
            borderwidth=1,
            command=lambda: self.quit()
        )
        self.close_this.pack(pady=5)

        self.run_type_show()

        trial_frame = tk.Frame(self.list_row)
        trial_frame.grid(row=0, column=2, sticky="ne")

        self.trial_title_label = tk.Label(
            trial_frame,
            text=f"{self.i18n.t("score_win.series")}:",
            font=("Helvetica", 10),
        )
        self.trial_title_label.pack(anchor="w")

        self.trials = tk.Listbox(
            trial_frame,
            height=10,
            width=30,
            activestyle="dotbox",
            font="Helvetica",
        )
        self.trials.pack(anchor="w")
        self.trials.bind("<ButtonRelease-1>", self.on_series_click)
        self.trials_show()

        initial_x = np.arange(0, 500)
        initial_y = np.random.randint(0, 13, size=500)

        self.chart = Chart(self, initial_x, initial_y, view_size=20)
        self.chart.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)

    def load_uma_list(self):
        from database.get_uma import load_umas
        data = load_umas(self.app_path)
        return [f"[{r[0]}]    {r[2]} {r[1]}" for r in data]            

    def refresh_uma_list(self):
        data = self.load_uma_list()
        self.uma_list.delete(0, tk.END)
        self.uma_list.insert(tk.END, *data)
        
        for i in range(self.uma_list.size()):
            if i % 2 == 0:
                self.uma_list.itemconfigure(i, background="#3a3a3a", foreground="white")
            else:
                self.uma_list.itemconfigure(i, background="#2a2a2a", foreground="white")

    def on_uma_click(self, event):
        selected_uma = self.uma_list.curselection()
        if selected_uma:
            full_text = self.uma_list.get(selected_uma)
            if self.act_sq.get() is True:
                pass
            try:
                raw_id = full_text.split('[')[1].split(']')[0]
                uma_id = int(raw_id)
                uma_name = load_uma_name(uma_id, self.app_path)

                labels, positions = load_uma_position(uma_id, self.app_path)

                if not labels:
                    messagebox.showwarning(f"{self.i18n.t("m_b.error")}", f"{self.i18n.t("m_b.no_data_for_uma")}: {uma_id}")
                    return

                dataset = {str(uma_name): positions}
                self.chart.update_data(labels, dataset)

                self.selected_trials = None
                self.selected_uma = uma_id
                self.selected_runtype = None

                self.update_clicked(f"{self.i18n.t("score_win.chosen_uma")}: {self.selected_uma}")
            except (IndexError, ValueError) as e:
                print(e)

    def run_type_show(self):
        try:
            from database.get_trials import load_type_of_run
            data = load_type_of_run(self.app_path)
            self.type_run.delete(0, tk.END)
            self.type_run.insert(tk.END, *data)
        except (IndexError, ValueError) as e:
            print(e)

    def on_runtype_click(self, event):
        selected_runtype = self.type_run.curselection()
        if selected_runtype:
            full_text = self.type_run.get(selected_runtype[0])
            try:
                raw_id = full_text.split('|')
                runtype_id = raw_id[0].strip()
                runtype_id = int(runtype_id)

                self.selected_trials = None
                self.selected_uma = None
                self.selected_runtype = runtype_id

                self.update_clicked(f"{self.i18n.t("score_win.chosen_distance")}: {runtype_id}")

                uma_ids = load_umas_by_distance(runtype_id, self.app_path)
                uma_ids = self._show_with_act_sq(self.act_sq, uma_ids)

                self._show_data_on_chart(uma_ids)
            except (IndexError, ValueError) as e:
                print(e)

    def trials_show(self):
        from database.get_trials import load_trials
        data = load_trials(self.app_path)
        self.trials.delete(0, tk.END)
        self.trials.insert(tk.END, *data)

    def on_series_click(self, event):
        selected_serie = self.trials.curselection()
        if selected_serie:
            full_text = self.trials.get(selected_serie[0])
            try:
                raw_id = full_text.split('|')
                trial_id = raw_id[0].strip()
                trial_id = int(trial_id)

                self.selected_trials = trial_id
                self.selected_runtype = None
                self.selected_uma = None

                self.update_clicked(f"{self.i18n.t("score_win.chosen_trial")}: {trial_id}")

                uma_ids = load_umas_by_trial(trial_id, self.app_path)
                uma_ids = self._show_with_act_sq(self.act_sq, uma_ids)

                self._show_data_on_chart(uma_ids)
            except (IndexError, ValueError) as e:
                print(e)

    def _show_with_act_sq(self, act_sq, uma_ids):
        if uma_ids is None:
            return []

        if act_sq.get() is True:
            if uma_ids:
                ids = {uma[0] for uma in uma_ids}
                filtered = [uma for pos, uma in self.json_squad.items()
                            if uma is not None and uma in ids]
                uma_ids = filtered
                return uma_ids
        else:
            uma_ids = [uma[0] for uma in uma_ids if uma is not None]
            return uma_ids

    def _show_data_on_chart(self, uma_ids):
        if not uma_ids:
            self.chart.update_data([], {})
            return

        raw_data = {}
        all_timestamps = set()
        for uma in uma_ids:
            self.uma_id = uma
            name = load_uma_name(self.uma_id, self.app_path)
            uma_name = name[0][0] if isinstance(name, list) else name

            unique_key = f"{uma_name} [{self.uma_id}]"

            labels, positions = load_uma_position(self.uma_id, self.app_path)
            uma_entry = dict(zip(labels, positions))
            raw_data[unique_key] = uma_entry
            
            all_timestamps.update(labels)

        sorted_timeline = sorted(list(all_timestamps))

        synchronized_umas = {}
        for unique_name, results in raw_data.items():
            sync_pos = []
            for timestamp in sorted_timeline:
                val = results.get(timestamp, None)
                sync_pos.append(val)

            synchronized_umas[unique_name] = sync_pos

        self.chart.update_data(sorted_timeline, synchronized_umas)

    def update_clicked(self, text):
        self.is_clicked.config(text=text)

    def quit(self):
        self.destroy()