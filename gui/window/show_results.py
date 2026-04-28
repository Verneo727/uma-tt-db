#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox

from gui.widgets.chart import Chart
from database.get_uma import (
    load_umas,
    load_uma_position,
    load_uma_name,
    load_umas_by_distance,
    load_umas_by_trial,
    load_uma_result_in_trial)
from database.get_team import load_team
from database.get_trials import (load_trials, load_distances)
from core.i18n import I18n
from core.statistics import Statistics
import numpy as np

class ShowResults(tk.Toplevel):
    def __init__(self, app_path, lang, master=None):
        super().__init__(master = master)
        self.master = master
        self.app_path = app_path
        self.lang = lang
        self.i18n = I18n(language=lang)
        self.stats = Statistics(self.app_path)

        self.title(f"{self.i18n.t("score_win.title")}")
        self.geometry("1000x800")

        self.uma_id = None
        self.distance_id = None
        self.selected_trials = None

        self.act_sq = tk.BooleanVar(value=False)
        self.json_squad = load_team(app_path)

        self.chart = Chart(self, [], {}, view_size=20)

        self._gui()
        self.refresh_uma_list()

    def _gui(self):
        self.umas_frame()
        self.distances_frame()
        self.statistics_frame()
        self.trials_frame()
        self.refresh_uma_list()

    def umas_frame(self):
        self.list_row = tk.Frame(self)
        self.list_row.pack(side="top", fill='x', padx=10, pady=10)
        self.list_row.columnconfigure(0, weight=1)
        self.list_row.columnconfigure(1, weight=1)
        self.list_row.columnconfigure(2, weight=1)
        self.list_row.columnconfigure(3, weight=1)

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

        self.uma_list_average = tk.Label(
            uma_list_frame,
            text="",
            font="Helvetica",
        )
        self.uma_list_average.pack(anchor="w", pady=2)

    def distances_frame(self):
        distances_frame = tk.Frame(self.list_row)
        distances_frame.grid(row=0, column=1, sticky="n")

        self.distances_title_label = tk.Label(
            distances_frame,
            text=f"{self.i18n.t("score_win.rodzaje")}:",
            font=("Helvetica", 10)
        )
        self.distances_title_label.pack(anchor="w")

        self.distances = tk.Listbox(
            distances_frame,
            height=5,
            width=12,
            activestyle="dotbox",
            font="Helvetica",
        )
        self.distances.pack(anchor="w")
        self.distances.bind("<ButtonRelease-1>", self.on_distances_click)

        self.is_clicked = tk.Label(
            distances_frame,
            text=f"{self.i18n.t("score_win.choose")}",
            width=22,
            font=("Helvetica", 10),
            relief="solid",
            borderwidth=1,
            background="#2a2a2a",
            fg="white"
        )
        self.is_clicked.pack(pady=5)

        self.actual_squad_btn = tk.Checkbutton(
            distances_frame,
            text=f"{self.i18n.t("score_win.dotyczy")}",
            width=22,
            font=("Helvetica", 10),
            command=lambda: self._show_with_act_sq(self.act_sq, uma_ids=None),
            variable=self.act_sq,
        )
        self.actual_squad_btn.pack(pady=2)

        self.close_this_btn = tk.Button(
            distances_frame,
            text=f"{self.i18n.t("score_win.back")}",
            relief="solid",
            borderwidth=1,
            command=lambda: self.quit()
        )
        self.close_this_btn.pack(pady=5)

        self.distances_show()

    def statistics_frame(self):
        statistics_frame = tk.Frame(self.list_row)
        statistics_frame.grid(row=0, column=2, sticky="ns")

        self.statistics_title_label = tk.Label(
            statistics_frame,
            text=f"{self.i18n.t('statistics.title')}:",
            font=("Helvetica", 10),
        )
        self.statistics_title_label.pack(anchor="w")

        all_tt_races = self.stats.all_tt_races()
        self.all_tt_races_lbl = tk.Label(
            statistics_frame,
            text=f"{self.i18n.t('statistics.all_tt_races')}: {all_tt_races}",
            font=("Helvetica", 8),
        )
        self.all_tt_races_lbl.pack(anchor="w")

        all_tt_runs = self.stats.all_single_runs()
        self.all_tt_runs_lbl = tk.Label(
            statistics_frame,
            text=f"{self.i18n.t('statistics.all_runs')}: {all_tt_runs}",
            font=("Helvetica", 8),
        )
        self.all_tt_runs_lbl.pack(anchor="w")

        all_days = self.stats.all_race_days()
        self.all_days_lbl = tk.Label(
            statistics_frame,
            text=f"{self.i18n.t('statistics.all_days')}: {all_days}",
            font=("Helvetica", 8),
        )
        self.all_days_lbl.pack(anchor="w")

        percent_win = self.stats.win_percent()
        self.percent_of_win = tk.Label(
            statistics_frame,
            text=f"{self.i18n.t('statistics.percent_win')}: {percent_win}%",
            font=("Helvetica", 8),
        )
        self.percent_of_win.pack(anchor="w")

        percent_second = self.stats.second_percent()
        self.percent_of_2nd_places = tk.Label(
            statistics_frame,
            text=f"{self.i18n.t('statistics.percent_2nd')}: {percent_second}%",
            font=("Helvetica", 8),
        )
        self.percent_of_2nd_places.pack(anchor="w")

        percent_third = self.stats.third_percent()
        self.percent_of_3rd_places = tk.Label(
            statistics_frame,
            text=f"{self.i18n.t('statistics.percent_3rd')}: {percent_third}%",
            font=("Helvetica", 8),
        )
        self.percent_of_3rd_places.pack(anchor="w")

        self.statistics_button = tk.Button(
            statistics_frame,
            text=f"{self.i18n.t('statistics.detailed')}",
            relief="solid",
            borderwidth=1,
            command=lambda: self.statistics(),
        )
        self.statistics_button.pack(side="bottom", expand=True)

    def trials_frame(self):
        trial_frame = tk.Frame(self.list_row)
        trial_frame.grid(row=0, column=3, sticky="ne")

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
        self.trials.bind("<ButtonRelease-1>", self.on_trial_click)
        self.trials_show()

        initial_x = np.arange(0, 500)
        initial_y = np.random.randint(0, 13, size=500)

        self.chart = Chart(self, initial_x, initial_y, view_size=20)
        self.chart.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)

    def load_uma_list(self):
        data = load_umas(self.app_path)
        return [f"[{r[0]}]    {r[2]} {r[1]}" for r in reversed(data)]

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

                labels, positions, score, tiers = load_uma_position(uma_id, self.app_path)

                if not labels:
                    messagebox.showwarning(f"{self.i18n.t("m_b.error")}",
                                           f"{self.i18n.t("m_b.no_data_for_uma")}: {uma_id}")
                    return

                clean_scores = [s for s in score if s is not None]
                if clean_scores:
                    average_val = sum(clean_scores) / len(clean_scores)
                    display_avg = f"{average_val:.0f}"
                    self.uma_list_average.config(
                    text=f"{self.i18n.t('score_win.uma_list_avr')}: {display_avg}",
                )
                else:
                    self.uma_list_average.config(text="")

                dataset = {str(uma_name): positions}
                self.chart.update_data(labels, dataset,
                                       scores=score, bar_bg_tiers=tiers)

                self.selected_trials = None
                self.selected_uma = uma_id
                self.selected_distance = None

                self.update_clicked(f"{self.i18n.t("score_win.chosen_uma")}: {self.selected_uma}")
            except (IndexError, ValueError) as e:
                print(e)

    def distances_show(self):
        try:
            data = load_distances(self.app_path)
            formatted = []
            for row in data:
                line = f"{row[0]}  | {row[1]}"
                formatted.append(line)
            data = formatted
            self.distances.delete(0, tk.END)
            self.distances.insert(tk.END, *data)
        except (IndexError, ValueError) as e:
            print(e)

    def on_distances_click(self, event):
        selected_distance = self.distances.curselection()
        if selected_distance:
            full_text = self.distances.get(selected_distance[0])
            try:
                self.uma_list_average.config(text="")
                raw_id = full_text.split('|')
                distance_id = raw_id[0].strip()
                distance_id = int(distance_id)

                self.selected_trials = None
                self.selected_uma = None
                self.selected_distance = distance_id

                self.update_clicked(f"{self.i18n.t("score_win.chosen_distance")}: {distance_id}")

                uma_ids = load_umas_by_distance(distance_id, self.app_path)
                uma_ids = self._show_with_act_sq(self.act_sq, uma_ids)

                self._show_data_on_chart(uma_ids)
            except (IndexError, ValueError) as e:
                print(e)

    def trials_show(self):
        data = load_trials(self.app_path)
        formatted = []
        for row in data:
            line = f"{row[0]}   | {row[1]} | {row[2]}"
            formatted.append(line)
        data = formatted
        self.trials.delete(0, tk.END)
        self.trials.insert(tk.END, *data)

    def on_trial_click(self, event):
        selected_trial = self.trials.curselection()
        if selected_trial:
            full_text = self.trials.get(selected_trial[0])
            try:
                self.uma_list_average.config(text="")
                raw_id = full_text.split('|')
                trial_id = raw_id[0].strip()
                trial_id = int(trial_id)

                self.selected_trials = trial_id
                self.selected_distance = None
                self.selected_uma = None

                self.update_clicked(f"{self.i18n.t("score_win.chosen_trial")}: {trial_id}")
                trial_data = self._get_full_trial_info(trial_id)
                trial_data.sort(key=lambda x: x['dist_id'])

                uma_names = [f"{d['name']} ({d['dist_name']})" for d in trial_data]
                positions = [d['pos'] for d in trial_data]

                self.chart.update_data(uma_names, positions, is_bar=True, bar_bg_tiers=None)

            except (IndexError, ValueError) as e:
                print(e)

    def _get_full_trial_info(self, trial_id):
        uma_ids = load_umas_by_trial(trial_id, self.app_path)
        uma_ids = self._show_with_act_sq(self.act_sq, uma_ids)
        results = []
        dist_map = {0: "Sprint", 1: "Mile", 2: "Medium", 3: "Long", 4: "Dirt"}

        for uma_id in uma_ids:
            u_id = uma_id[0] if isinstance(uma_id, (list, tuple)) else uma_id
            name = load_uma_name(u_id, self.app_path)

            pos, dist_id = load_uma_result_in_trial(u_id, trial_id, self.app_path)

            results.append({
                'name': name,
                'pos': pos,
                'dist_id': dist_id,
                'dist_name': dist_map.get(dist_id, "??")
            })
        return results

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

            labels, positions, _, _ = load_uma_position(self.uma_id, self.app_path)
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

    def statistics(self):
        print("Statistics window. WIP")

    def update_clicked(self, text):
        self.is_clicked.config(text=text)

    def quit(self):
        self.destroy()