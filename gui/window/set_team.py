#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
import json

from core.tooltip import ToolTip
from core.i18n import I18n
from database.get_uma import load_umas
from setup.config import load_json

class ActualTeam(tk.Toplevel):
    def __init__(self, app_path, lang, master=None):
        super().__init__(master=master)
        self.master = master
        self.app_path = app_path
        self.lang = lang
        self.i18n = I18n(language=lang)
        self.title(f"{self.i18n.t("actual_team.title")}")
        self.geometry("500x560")

        self.umas = load_umas(app_path)

        self._gui()
        self.after(0, self._load_results())

    def _gui(self):
        text = f"{self.i18n.t("actual_team.info")}"
        self.info = tk.Label(
            self,
            text=text,
            font=("Helvetica", 10, "italic"),
            anchor="n",
        )
        text2 = f"{self.i18n.t("actual_team.info2")}"
        self.info2 = tk.Label(self,
            text=text2,
            font=("Helvetica", 10, "bold italic"),
            anchor="n",
            )
        self.info.config(padx=10, pady=10)
        self.info.pack()
        self.info2.config(padx=10, pady=2)
        self.info2.pack()

        delete_text = f"{self.i18n.t("actual_team.delete_txt")}"
        self.del_text_lbl = tk.Label(
            self,
            text=delete_text,
            font=("Helvetica", 8, "italic"),
            anchor="n",
        )
        self.del_text_lbl.config(padx=10, pady=2)
        self.del_text_lbl.pack()

        self.DIST_MAP = {
            "SPRINT": 0,
            "MILE": 1,
            "MEDIUM": 2,
            "LONG": 3,
            "DIRT": 4
        }

        tooltips = {
            "FR": "Front Runner",
            "PC": "Pace Chaser",
            "LS": "Late Surger",
            "EC": "End Closer"
        }

        self.combos = {}

        rows = [
            ("SPRINT", "MILE"),
            ("MEDIUM", "LONG"),
            ("DIRT",)
        ]

        for row_cats in rows:
            row_frame = tk.Frame(self)
            row_frame.pack(fill="x", padx=10, pady=5)
            for cat in row_cats:
                self._build_category(row_frame, cat, tooltips)

        btn_frame = tk.Frame(self)
        btn_frame.pack(side="left", fill="both", expand=True, padx=2, pady=2)

        tk.Button(
            btn_frame,
            text=f"{self.i18n.t("actual_team.exit")}",
            relief="solid",
            borderwidth=1,
            command=self._exit,
            ).pack(side="left", expand=True, padx=2)

        tk.Button(
            btn_frame,
            text=f"{self.i18n.t("actual_team.save")}",
            font=("Helvetica", 10, "bold"),
            relief="solid",
            borderwidth=2,
            command=self._save,
        ).pack(side="left", expand=True, padx=2)

    def _build_category(self, parent, name, tooltips):
        frame = tk.LabelFrame(
            parent,
            text=name,
            font=("Helvetica", 10, "bold"),
            relief="solid",
            borderwidth=1,
            labelanchor="nw",
        )
        frame.pack(side="left", fill="both", expand=True, padx=2, pady=2)

        self.combos[name] = {}

        distance_id = self.DIST_MAP.get(name)
        filtered_data = [u for u in self.umas if u[3] == distance_id][::-1]
        display_values = [f"{u[2]} {u[1]}" for u in filtered_data]

        for i, (code, full_name) in enumerate(tooltips.items()):
            lbl = tk.Label(frame, text=f"{code}: ", font=("Helvetica", 10))
            lbl.grid(row=i, column=0, sticky="w", padx=(5, 2), pady=1)
            ToolTip(lbl, full_name)

            cb = ttk.Combobox(frame, values=display_values, state="readonly", width=15)
            cb.grid(row=i, column=1, sticky="ew", padx=2, pady=1)

            lbl.bind("<Button-1>", lambda e, c=cb: self._reset_combo(e, c))

            self.combos[name][code] = {
                "widget": cb,
                "data": filtered_data
            }

        frame.columnconfigure(1, weight=1)

    def _save(self):
        results = {}
        for category, roles in self.combos.items():
            for role, combo in roles.items():
                key = f"{category.lower()}_{role.lower()}_uma"
                cb = combo["widget"]
                data = combo["data"]

                idx = cb.current()

                results[key] = data[idx][0] if idx != -1 else None

        print(results)
        self._save_results(results, self.app_path)

    def _load_results(self):
        try:
            json_path = load_json(self.app_path)

            with open(json_path, "r", encoding="utf-8") as f:
                results = json.load(f)

            for category, roles in self.combos.items():
                for role, combo in roles.items():
                    key = f"{category.lower()}_{role.lower()}_uma"
                    uma_id = results.get(key)

                    if uma_id is not None:
                        cb = combo["widget"]
                        data = combo["data"]
                        for i, row in enumerate(data):
                            if str(row[0]) == str(uma_id):
                                cb.current(i)
                                break

        except Exception as e:
            print(e)

    def _save_results(self, results, app_path):
        json_path = load_json(self.app_path)
        if not json_path:
            return

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)

    def _reset_combo(self, event, combo):
        combo.set("")

    def _exit(self):
        self.destroy()