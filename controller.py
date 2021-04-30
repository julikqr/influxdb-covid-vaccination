from model import Model
from view import View


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View(self)

    def start_gui(self):
        self.view.start_gui()

    def button_clicked(self, button):
        status = self.model.execute_query(button)
        self.view.set_status(status)
