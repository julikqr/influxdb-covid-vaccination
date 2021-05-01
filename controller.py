from model import Model
from view import View


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View(self)
        self.dbstatus = False

        self.connect_to_db()
        self.view.start_gui()

    def connect_to_db(self):
        self.dbstatus = self.model.connect_to_db()
        if self.dbstatus:
            print("Succesfully connected to InfluxDB")
            self.view.set_status("Succesfully connected to InfluxDB")
        else:
            self.view.set_status("Connection to InfluxDb failed")
            print("Connection to InfluxDb failed")

    def button_clicked(self, button):
        status = self.model.execute_query(button)
        self.view.set_status(status)
