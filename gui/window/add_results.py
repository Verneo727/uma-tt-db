#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from database.get_uma import (load_umas_by_id)
from database.get_team import load_team
from database.get_distances import get_distances
from database.get_trials import load_trials_short
from database.add_results import add_results_to_db

from core.i18n import I18n
from core.tooltip import ToolTip

class AddResults(tk.Toplevel):
    def __init__(self, app_path, lang, master=None):
        super().__init__(master=master)
        self.master = master
        self.i18n = I18n(language=lang)

        self.title(f"{self.i18n.t("add_results.title")}")
        self.geometry("520x750")

        self.team = load_team(app_path)
        self.combo_trials = load_trials_short(app_path)
        self.distances = get_distances(app_path)

        self.entries = {}
        self.dist_frames = {}
        self.pos_entries = []
        self.score_entries = []

        self._gui(app_path)

    def _gui(self, app_path):
        info_text = f"{self.i18n.t("add_results.info")}"
        self.info_label = tk.Label(
            self,
            text=info_text,
            font=("Helvetica", 10, "italic"),
            anchor="n",
        )
        self.info_label.config(padx=10, pady=10)
        self.info_label.pack()

        self.info_row_label = tk.Label(
            self,
            anchor="n",
        )
        self.info_row_label.pack()

        self.help_label = tk.Label(
            self.info_row_label,
            text=" ❓ ",
            fg="red",
            bg="white",
            relief="groove",
            borderwidth=2,
        )
        ToolTip(self.help_label, f"{self.i18n.t("add_results.help")}")
        self.help_label.pack(side="left", expand=True)

        self.trial_combo = ttk.Combobox(
            self.info_row_label,
            values=self.combo_trials,
            state="readonly",
            width=30,
        )
        self.trial_combo.pack(side="left", expand=True, padx=20)

        uma_ids = [uid for uid in self.team.values() if uid is not None]
        self.umas_dict = load_umas_by_id(uma_ids, app_path)

        dist_names = {row[0]: row[1] for row in self.distances}

        for position, uma_id in self.team.items():
            if uma_id is None:
                continue

            uma_data = self.umas_dict.get(uma_id, {})
            dist_id = uma_data.get("distance")
            dist_name = dist_names.get(dist_id, "Unknown distance")

            if dist_id not in self.dist_frames:
                self.dist_frame = tk.LabelFrame(self,
                                                text=dist_name.upper(),
                                                font=("Helvetica", 12, "bold"),
                                                )
                self.dist_frame.pack(fill="x", padx=10, pady=5)
                self.dist_frames[dist_id] = self.dist_frame

            target_frame = self.dist_frames[dist_id]

            if position not in self.entries:
                self.entries[position] = {}

            self.row_frame = tk.Frame(target_frame)
            self.row_frame.pack(fill="x", pady=2)

            name = uma_data.get("name", str(uma_id))
            rating = uma_data.get("rating", "?")

            self.uma_name_label = tk.Label(
                self.row_frame,
                text=f"{name}   ({rating})",
                width=25,
                anchor="w",
            )
            self.uma_name_label.pack(side="left")

            pos_hint = self.i18n.t('add_results.pos')
            self.uma_position_entry = tk.Entry(self.row_frame, fg="grey", width=10)
            self.pos_entries.append(self.uma_position_entry)
            self.uma_position_entry.insert(0, pos_hint)
            self.uma_position_entry.pack(side="left", padx=(20, 5))
            self.uma_position_entry.bind('<FocusIn>', lambda event, p=pos_hint: self._on_entry_click(event, p))
            self.uma_position_entry.bind('<FocusOut>', lambda event, p=pos_hint: self._on_focus_out(event, p))

            score_hint = self.i18n.t('add_results.score')
            self.uma_score_entry = tk.Entry(self.row_frame, fg="grey", width=20)
            self.score_entries.append(self.uma_score_entry)
            self.uma_score_entry.insert(0, score_hint)
            self.uma_score_entry.pack(side="left", padx=5)
            self.uma_score_entry.bind('<FocusIn>', lambda event, p=score_hint: self._on_entry_click(event, p))
            self.uma_score_entry.bind('<FocusOut>', lambda event, p=score_hint: self._on_focus_out(event, p))

            self.entries[position][uma_id] = {
                "pos": self.uma_position_entry,
                "score": self.uma_score_entry
            }

        self.button_row_label = tk.Label(self)
        self.button_row_label.pack(padx=2, pady=15)

        self.back_to_menu = tk.Button(
            self.button_row_label,
            text=f"{self.i18n.t("add_results.exit")}",
            font=("Helvetica", 10),
            relief="solid",
            borderwidth=1,
            command=self._exit,
        )
        self.back_to_menu.pack(side="left", expand=True, padx=20)

        self.save = tk.Button(
            self.button_row_label,
            text=f"{self.i18n.t("add_results.save")}",
            font=("Helvetica", 10, "bold"),
            borderwidth=2,
            command=lambda: self._save(app_path),
        )
        self.save.pack(side="left", expand=True, padx=20)
        self.bind("<Return>", lambda event: self._save(app_path))

        # POS column TAB bind
        for i in range(len(self.pos_entries)):
            if i + 1 < len(self.pos_entries):
                next_widget = self.pos_entries[i+1]
            else:
                next_widget = self.score_entries[0] if self.score_entries else None

            if next_widget:
                self.pos_entries[i].bind("<Tab>", lambda e, n=next_widget: self._focus_next(e, n))

        # SCORE column TAB Bind
        for i in range(len(self.score_entries)):
            if i + 1 < len(self.score_entries):
                next_widget = self.score_entries[i+1]
            else:
                next_widget = self.pos_entries[0]

            if next_widget:
                self.score_entries[i].bind("<Tab>", lambda e, n=next_widget: self._focus_next(e, n))

    def _save(self, app_path, event=None):
        """Save the results to the database"""
        selected_trial = self.trial_combo.get()
        if not selected_trial:
            messagebox.showerror(f"{self.i18n.t("m_b.no_trial")}", f"{self.i18n.t("m_b.select_trial")}!")
            return
        id_trial = selected_trial.split()[0]

        pos_hint = self.i18n.t('add_results.pos')
        score_hint = self.i18n.t('add_results.score')

        inputs_to_db = []
        for pos, uma_inputs in self.entries.items():
            for uma_id, entries in uma_inputs.items():
                res_pos = entries["pos"].get().strip()
                res_score = entries["score"].get().strip()

                if res_pos and res_pos != pos_hint:
                    try:
                        val_pos = int(res_pos)
                        if res_score == score_hint or res_score == "":
                            val_score = None
                        else:
                            val_score = int(res_score)

                        uma_info = self.umas_dict.get(uma_id, {})
                        id_distance = uma_info.get("distance")
                        inputs_to_db.append((id_trial, uma_id, res_pos, val_score, id_distance))

                    except ValueError:
                        messagebox.showerror(
                            self.i18n.t("add_results.error_title"),
                            self.i18n.t("add_results.error")
                        )

        if inputs_to_db:
            add_results_to_db(inputs_to_db, app_path)
            self._clear_inputs()
        else:
            messagebox.showerror(f"{self.i18n.t("m_b.no_data")}", f"{self.i18n.t("m_b.all_entries")}")

    def _clear_inputs(self):
        """
        Clears text fields after saving to the DB.
        Advances the combobox to the next trial in the sequence.
        """
        selected_trial = self.trial_combo.get()
        try:
            current_trial_index = self.combo_trials.index(selected_trial)
            if current_trial_index > 0:
                next_value = self.combo_trials[current_trial_index - 1]
                self.trial_combo.set(next_value)
            else:
                self.trial_combo.set("")
        except ValueError:
            if self.combo_trials:
                self.trial_combo.set(self.combo_trials[-1])
            else:
                self.trial_combo.set("")

        pos_hint = self.i18n.t('add_results.pos')
        score_hint = self.i18n.t('add_results.score')

        for pos, uma_inputs in self.entries.items():
            for uma_id, entries in uma_inputs.items():
                entries["pos"].delete(0, 'end')
                entries["pos"].insert(0, pos_hint)
                entries["pos"].config(fg="grey")
                entries["score"].delete(0, 'end')
                entries["score"].insert(0, score_hint)
                entries["score"].config(fg="grey")
        if self.entries:
            try:
                first_pos_dict = next(iter(self.entries.values()))
                first_input_entry = next(iter(first_pos_dict.values()))
                first_input_entry["pos"].focus_set()
            except StopIteration:
                pass

    def _on_entry_click(self, event, pos_hint):
        widget = event.widget
        if widget.get() == pos_hint:
            widget.delete(0, tk.END)
            widget.config(fg="black")

    def _on_focus_out(self, event, pos_hint):
        widget = event.widget
        if widget.get() == '':
            widget.insert(0, pos_hint)
            widget.config(fg="grey")

    def _focus_next(self, event, target):
        target.focus_set()
        return "break"

    def _exit(self):
        self.destroy()