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
            self.view.set_status("Succesfully connected to InfluxDB")
        else:
            self.view.set_status(
                "Connection failed - Press any button to connect")

    def button_clicked(self, button):
        if self.dbstatus:
            if button == "Create vaccine deliveries":
                self.create_vaccine_deliveries()
            if button == "Read - Germany BW vaccine deliveries":
                self.read_vaccine_deliveries_debw()
            if button == "Delete vaccine deliveries":
                self.delete_vaccine_deliveries()
            if button == "Read - German states with most vaccines":
                self.read_states_most_vaccines()
            if button == "Read - 14d mean vaccine delivery":
                self.read_vaccine_mean()
            if button == "Read - Cumulated deliveries grouped by vaccine":
                self.read_cumulated_deliveries_by_vaccine()
        else:
            self.connect_to_db()

    def create_vaccine_deliveries(self):
        if self.model.create_vaccine_deliveries():
            self.view.set_status("DB is filled with vaccine delivery data")
        else:
            self.view.set_status("Could not write Vaccine delivery data to DB")

    def read_vaccine_deliveries_debw(self):
        data = self.model.read_vaccine_deliveries_debw()
        if data.size == 0:
            self.view.set_status("Please create data first")
        else:
            print(data)
            self.view.set_status("Read Germany BW vaccine deliveries")
            self.view.plot_line_chart(
                data, "time", "vaccines", "Germany Baden-Wuerttemberg vaccine deliveries")

    def read_states_most_vaccines(self):
        data = self.model.read_states_most_vaccines()
        if len(data) == 0:
            self.view.set_status("Please create data first")
        else:
            self.view.set_status("Read states with most vaccines")
            self.view.plot_bar_chart(
                data, "region", "vaccines", "Vaccines per state")

    def read_vaccine_mean(self):
        data = self.model.read_vaccine_mean()
        self.view.plot_line_chart(
            data, "time", "vaccines", "Germany 14d mean vaccine deliveries")

    def read_cumulated_deliveries_by_vaccine(self):
        data = self.model.read_cumulated_deliveries_by_vaccine()
        self.view.plot_line_chart(
            data, "time", "vaccine", "Germany cumulated vaccine deliveries in DE-BW")

    def delete_vaccine_deliveries(self):
        if(self.model.delete("vaccine_delivery")):
            self.view.set_status("Vaccine deliveries deleted")
        else:
            self.view.set_status("Failed to delete vaccine deliveries")
