#!/usr/bin/env python3

import tkinter as tk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FixedFormatter, FixedLocator, MaxNLocator

class Chart(tk.Frame):
    def __init__(self, parent, x_data=None, y_data=None, view_size=20, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.x_data = list(x_data) if x_data is not None else []
        self.y_data = y_data if y_data is not None else {}
        self.is_bar = False             # Uma's places, different chart
        self.view_size = view_size
        self.ax2 = None                 # Score axis

        self.x_indices = list(range(len(self.x_data)))

        self.fig = Figure(figsize=(5, 2), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.ax.set_ylim(0, 12)
        self.ax.set_yticks(range(13))
        self.ax.grid(True, linestyle='--', alpha=0.5)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self._on_scroll)
        self.scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        if self.x_data:
            self.update_data(self.x_data, self.y_data)

    def update_data(self, new_x, new_y, is_bar=False, scores=None):
        self.x_data = list(new_x)
        self.y_data = new_y
        self.is_bar = is_bar
        self.scores = scores

        if self.ax2 is not None:
            self.ax2.remove()
            self.ax2 = None

        if self.is_bar:
            self.x_indices = list(range(len(self.x_data)))
        else:
            max_len = max([len(v) for v in self.y_data.values()]) if (isinstance(self.y_data, dict) and len(self.y_data) > 0) else 0
            self.x_indices = list(range(max_len))

        self.ax.clear()
        self.ax.set_ylim(0, 12)
        self.ax.invert_yaxis()
        self.ax.set_yticks(range(13))
        self.ax.grid(True, linestyle='--', alpha=0.3)

        if is_bar:
            bottom_val = 12
            heights = [p - bottom_val for p in new_y]
            bar_colors = []
            for pos in new_y:
                if pos == 1: bar_colors.append('gold')
                elif pos == 2: bar_colors.append('silver')
                elif pos == 3: bar_colors.append('#CD7F32')
                else: bar_colors.append('skyblue')

            bars = self.ax.bar(
                range(len(new_x)),
                heights,
                bottom=bottom_val,
                color=bar_colors,
                width=0.4,
                zorder=2)

            for bar, pos in zip(bars, new_y):
                text_color = 'darkgoldenrod' if pos == 1 else 'black'
                self.ax.text(bar.get_x() + bar.get_width()/2., pos + 0.1,
                             f'{int(pos)}', ha='center',
                             va='bottom', fontweight='bold',
                             color=text_color)

            self.ax.set_xticks(range(len(new_x)))
            self.ax.set_xticklabels(new_x, rotation=45, ha='right')
        else:
            # Scores as background bars on secondary Y axis
            if scores is not None and len(scores) > 0:
                self.ax2 = self.ax.twinx()
                score_x = list(range(len(scores)))
                score_vals = [s if s is not None else 0 for s in scores]
                max_score = max(score_vals) if score_vals else 1
                self.ax2.set_ylim(0, max(1, max_score * 1.25)) # in future add this as a user config
                bars = self.ax2.bar(
                    score_x,
                    score_vals,
                    color='steelblue',
                    alpha=0.20,
                    width=0.8,
                    zorder=2,
                    label='Score',
                )
                # Label each bar with the score value
                for bar, val in zip(bars, score_vals):
                    if val:
                        self.ax2.text(
                            bar.get_x() + bar.get_width() / 2.,
                            bar.get_height(),
                            f'{int(val):,}',
                            ha='center',
                            va='bottom',
                            fontsize=8,
                            color='steelblue',
                            alpha=0.75,
                            zorder=2,
                            clip_on=True,
                        )
                self.ax2.set_ylabel('Score', fontsize=7, color='steelblue', labelpad=2)
                self.ax2.tick_params(axis='y', labelsize=6, colors='steelblue')

                self.ax2.yaxis.set_major_locator(MaxNLocator(nbins=4, integer=True))

                self.ax2.set_zorder(self.ax.get_zorder() - 1)
                self.ax.set_frame_on(False)

            if isinstance(self.y_data, dict):
                for name, values in self.y_data.items():
                    current_x = list(range(len(values)))

                    line, = self.ax.plot(current_x, values, marker='o', markersize=3, label=str(name), linewidth=1.5, zorder=2)

                    current_color = line.get_color()
                    def plot_medal(place, medal_color, size):
                        m_x = [current_x[i] for i, v in enumerate(values) if v is not None and int(v) == place]
                        if m_x:
                            self.ax.scatter(m_x, [place] * len(m_x),
                                            color=medal_color, s=size, zorder=3,
                                            edgecolors=current_color, linewidths=1)

                    gold_x = [self.x_indices[i] for i, v in enumerate(values) if v is not None and int(v) == 1]
                    gold_y = [1] * len(gold_x)
                    if gold_x:
                        self.ax.scatter(gold_x, gold_y, color='gold', s=50, zorder=3, edgecolors='darkgoldenrod', linewidths=1)

                    silver_x = [self.x_indices[i] for i, v in enumerate(values) if v is not None and int(v) == 2]
                    silver_y = [2] * len(silver_x)
                    if silver_x:
                        self.ax.scatter(silver_x, silver_y, color='silver', s=50, zorder=3, edgecolors='dimgray', linewidths=0.5)

                    bronze_x = [self.x_indices[i] for i, v in enumerate(values) if v is not None and int(v) == 3]
                    bronze_y = [3] * len(bronze_x)
                    if bronze_x:
                        self.ax.scatter(bronze_x, bronze_y, color='#CD7F32', s=50, zorder=3)

                if self.y_data:
                    self.ax.legend(loc='lower left', fontsize='small', ncol=2 if len(self.y_data) >5 else 1)

        self.fig.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.25)
        self.update_view()

    def _set_x_limits(self, start_idx):
        if not self.x_data: return
        end_idx = start_idx + self.view_size
        self.ax.set_xlim(start_idx - 0.5, end_idx - 0.5)

        if self.ax2 is not None:
            self.ax2.set_xlim(start_idx - 0.5, end_idx - 0.5)

        visible_indices = list(range(start_idx, min(end_idx, len(self.x_data))))

        if visible_indices:
            self.ax.xaxis.set_major_locator(FixedLocator(visible_indices))
            self.ax.xaxis.set_major_formatter(FixedFormatter([str(self.x_data[i]) for i in visible_indices]))

        self.ax.tick_params(axis='x', labelrotation=90, labelsize=8)
        self.fig.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.25)
        self.canvas.draw_idle()

    def _on_scroll(self, *args):
        total = len(self.x_indices)
        if total <= self.view_size:
            return
        if args[0] == 'moveto':
            pos = float(args[1])
        elif args[0] == 'scroll':
            current_pos = self.scrollbar.get()[0]
            step = 1.0 / (total - self.view_size)
            if args[2] == 'units':
                pos = current_pos + (int(args[1]) * step)
            else:
                pos = current_pos + (int(args[1]) * step * 5)
        else:
            return

        pos = max(0.0, min(1.0, pos))

        start_idx = int(pos * (total - self.view_size))

        self.scrollbar.set(start_idx/total, (start_idx + self.view_size) / total)
        self._set_x_limits(start_idx)

    def update_view(self):
        total = len(self.x_indices)
        if total <= self.view_size:
            self.ax.set_xlim(-0.5, self.view_size - 0.5)
            self.scrollbar.set(0.0, 1.0)
            self._set_x_limits(0)
        else:
            start_idx = total - self.view_size
            self._set_x_limits(start_idx)
            self.scrollbar.set(start_idx / total, 1.0)

        if hasattr(self, 'canvas'):
            self.canvas.draw()