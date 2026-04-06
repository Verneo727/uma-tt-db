#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
from pathlib import Path
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
        self.geometry("500x500")

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
        self.info.config(padx=10, pady=10)
        self.info.pack()

        categories = {
            "SPRINT": ["FR", "PC", "LS", "EC"],
            "MILE": ["FR", "PC", "LS", "EC"],
            "MEDIUM": ["FR", "PC", "LS", "EC"],
            "LONG": ["FR", "PC", "LS", "EC"],
            "DIRT": ["FR", "PC", "LS", "EC"],
        }

        tooltips = {
            "FR": "Front Runner",
            "PC": "Pace Chaser",
            "LS": "Late Surger",
            "EC": "End Closer"
        }

        uma_values = [f"{row[2]} {row[1]}" for row in self.umas]
        self.combos = {}

        # SPRINT & MILE
        sm_row = tk.Frame(self)
        sm_row.pack(fill="x", padx=10, pady=10)
        self._build_category(sm_row, "SPRINT", uma_values, tooltips)
        self._build_category(sm_row, "MILE", uma_values, tooltips)

        # MEDIUM & LONG
        ml_row = tk.Frame(self)
        ml_row.pack(fill="x", padx=10, pady=10)
        self._build_category(ml_row, "MEDIUM", uma_values, tooltips)
        self._build_category(ml_row, "LONG", uma_values, tooltips)

        # DIRT + BUTTONS
        d_row = tk.Frame(self)
        d_row.pack(fill="x", padx=10, pady=10)
        self._build_category(d_row, "DIRT", uma_values, tooltips)

        btn_frame = tk.Frame(d_row)
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

    def _build_category(self, parent, name, values, tooltips):
        frame = tk.Frame(parent, relief="solid", borderwidth=1)
        frame.pack(side="left", fill="both", expand=True, padx=2, pady=2)

        tk.Label(
            frame,
            text=name,
            font=("Helvetica", 10, "bold")
            ).pack(anchor="w", padx=2)

        self.combos[name] = {}

        for code, full_name in tooltips.items():
            row_frame = tk.Frame(frame)
            row_frame.pack(anchor="w", padx=2, pady=1)

            lbl = tk.Label(row_frame, text=f"{code}: ", font=("Helvetica", 10))
            lbl.pack(side="left", padx=2)
            ToolTip(lbl, full_name)

            cb = ttk.Combobox(row_frame, values=values, state="readonly")
            cb.pack()

            lbl.bind("<Button-1>", lambda e, c=cb: self._reset_combo(e, c))

            self.combos[name][code] = cb

    def _save(self):
        results = {}
        for category, roles in self.combos.items():
            for role, combo in roles.items():
                key = f"{category.lower()}_{role.lower()}_uma"
                idx = combo.current()

                results[key] = self.umas[idx][0] if idx != -1 else None

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
                        for i, row in enumerate(self.umas):
                            if str(row[0]) == str(uma_id):
                                combo.current(i)
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