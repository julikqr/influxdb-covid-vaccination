
import tkinter as tk
from tkinter import ttk


class View(tk.Tk):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self._category_button_names = [
            "Create vaccine deliveries", "Read", "Update", "Delete vaccine deliveries"]
        self.status = tk.StringVar()

        self.title("My InfluxDB GUI")
        self.status.set("Please select a query to execute")
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
