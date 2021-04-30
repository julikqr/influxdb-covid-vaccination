
import tkinter as tk
from tkinter import ttk


class View(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.title("My InfluxDB GUI")

        self.controller = controller
        self._category_buttons = []
        self._category_button_names = ["Create", "Read", "Update", "Delete"]

        self._create_frames()
        self._create_category_buttons()
        print("Hello from view")

    def start_gui(self):
        self.mainloop()

    def _create_frames(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=5, pady=5)

        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.pack(side='left')

        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side='left')

    def _create_category_buttons(self):
        for name in self._category_button_names:
            btn = ttk.Button(self.left_frame, text=name,
                             command=(
                                 lambda button=name: self.controller.category_button_clicked(
                                     button)
                             )
                             )
            btn.pack()
            self._category_buttons.append(btn)

        #btn = ttk.Button(self.left_frame, text='Read')
        # self._category_buttons.append(btn)

        #btn = ttk.Button(self.left_frame, text='Update')
        # self._category_buttons.append(btn)

        #btn = ttk.Button(self.left_frame, text='Delete')
        # self._category_buttons.append(btn)

        #[btn.pack() for btn in self._category_buttons]
