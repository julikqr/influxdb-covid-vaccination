
import tkinter as tk
from tkinter import ttk
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np


class View(tk.Tk):
    def __init__(self, controller):
        print("Initializing GUI...")
        super().__init__()

        self.controller = controller
        self._category_button_names = [
            "Create - vaccine deliveries",
            "Read - Germany BW vaccine deliveries",
            "Read - German states with most vaccines",
            "Read - 14d mean vaccine delivery",
            "Read - Cumulated deliveries grouped by vaccine",
            "Delete - vaccine deliveries",
            "Run Unittests"]
        self.status = tk.StringVar()

        self.title("My InfluxDB GUI")
        self._create_frames()
        self._create_label()
        self._create_buttons()

    def start_gui(self):
        self.mainloop()

    def set_status(self, status):
        self.status.set(status)

    def _create_frames(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=5, pady=5)

        self.label_frame = ttk.Labelframe(self.main_frame, text='Status')
        self.label_frame.pack()

        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack()

    def _create_label(self):
        label = ttk.Label(self.label_frame, textvariable=self.status, width=50)
        label.pack()

    def _create_buttons(self):
        for name in self._category_button_names:
            btn = ttk.Button(self.main_frame, text=name, width=50,
                             command=(
                                 lambda button=name: self.controller.button_clicked(
                                     button)
                             )
                             )
            btn.pack()

    def plot_line_chart(self, data, x_label, y_label, title):
        plt.clf()
        lines = data.line_name.unique()
        for line in lines:
            plt.plot(data[data.line_name == line].x_axis,
                     data[data.line_name == line].y_axis)
        plt.legend(lines)
        plt.xticks(rotation=45)
        plt.ylabel(y_label)
        plt.xlabel(x_label)
        plt.title(title)
        plt.show()

    def plot_bar_chart(self, data, x_label, y_label, title):
        plt.clf()
        x_axis_range = np.arange(len(data.x_axis))
        plt.bar(x_axis_range, data.y_axis, align='center')
        plt.xticks(x_axis_range, data.x_axis, rotation=90)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.show()
