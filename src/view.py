"""View
        * This file contains the View
        * initialize GUI
        * create frames and buttons
        * plots data 

    Attributes:
        * name: Julian S
        * date: 03.05.2021
        * version: 0.0.1 Beta - free
"""

import tkinter as tk
from tkinter import ttk
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np


class View(tk.Tk):
    def __init__(self, controller):
        """__init__
            * initialze tkinter with frames, labels and buttons

        Args:
            controller (Controller): controller of this class
        """
        print("Initializing GUI...")
        super().__init__()

        self.controller = controller
        self._category_button_names = [
            "Create - vaccine deliveries",
            "Read - Germany BW vaccine deliveries",
            "Read - German states with most vaccines",
            "Read - 14d sum vaccine delivery",
            "Read - Cumulated deliveries grouped by vaccine",
            "Delete - vaccine deliveries",
        ]
        self.status = tk.StringVar()

        self.title("My InfluxDB GUI")
        self._create_frames()
        self._create_label()
        self._create_buttons()

    def start_gui(self):
        """start_gui
            * start mainloop of gui
        """
        self.mainloop()

    def set_status(self, status):
        """set_status
            * display a status on the gui
        Args:
            status (str): A string to display on gui
        """
        self.status.set(status)

    def _create_frames(self):
        """create_frame
            * create frames for label and buttons
        """
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=5, pady=5)

        self.label_frame = ttk.Labelframe(self.main_frame, text='Status')
        self.label_frame.pack()

        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack()

    def _create_label(self):
        """create_label
            * create a label in which status notifications can be displayed
        """
        label = ttk.Label(self.label_frame, textvariable=self.status, width=50)
        label.pack()

    def _create_buttons(self):
        """create_buttons
            * creates buttons using self._category_button_names
        Raises:
            TypeError: Only accept string to be displayed in buttons
        """
        for name in self._category_button_names:
            if type(name) is str:
                btn = ttk.Button(self.main_frame, text=name, width=50,
                                 command=(
                                     lambda button=name: self.controller.button_clicked(
                                         button)
                                 )
                                 )
                btn.pack()
            else:
                raise TypeError()

    def plot_line_chart(self, data, x_label, y_label, title, plot=True):
        """plot a line chart
            * clears previous plot
            * plots a line chart with given data
            * creates a legend and labels
        Args:
            data (Pandas Dataframe): Data to plot. Needs columns: line_name, x_axis, y_axis
            x_label (str): A label for the x_axis 
            y_label (str): A label for the y_axis
            title (str): A title for this plot
            plot (bool, optional): Display this plot. Only unittests set this to False. Defaults to True.
        """
        plt.clf()
        lines = data.line_name.unique()
        # plot a line for every line_name (eg. plot a line for every vaccine )
        for line in lines:
            plt.plot(data[data.line_name == line].x_axis,
                     data[data.line_name == line].y_axis)
        plt.legend(lines)
        plt.xticks(rotation=45)
        plt.ylabel(y_label)
        plt.xlabel(x_label)
        plt.title(title)
        if plot:
            plt.show()

    def plot_bar_chart(self, data, x_label, y_label, title, plot=True):
        """plot a bar chart
            * clears previous plot
            * plots a bar chart with given data
            * creates a legend and labels
        Args:
            data (Pandas Dataframe): Data to plot. Needs columns: x_axis, y_axis
            x_label (str): A label for the x_axis 
            y_label (str): A label for the y_axis
            title (str): A title for this plot
            plot (bool, optional): Display this plot. Only unittests set this to False. Defaults to True.
        """
        plt.clf()
        x_axis_range = np.arange(len(data.x_axis))
        plt.bar(x_axis_range, data.y_axis, align='center')
        plt.xticks(x_axis_range, data.x_axis, rotation=90)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        if plot:
            plt.show()
