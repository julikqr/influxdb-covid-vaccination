from model import Model
from view import View


class Controller:
    def __init__(self):
        print("Hello from Controller")
        self.model = Model()
        self.view = View()

    def start_gui(self):
        self.view.start_gui()
