"""Controller
        * This file contains the Controller 
        * control the view and model
        * handle user input

    Attributes:
        * name: Julian S
        * date: 03.05.2021
        * version: 0.0.1 Beta - free
"""

from model import Model
from view import View


class Controller:
    def __init__(self, start_gui=True):
        """__init__
            * Create Model and View
            * Connect to database
            * Start GUI
        Args:
            start_gui (bool, optional): Define wheter GUI should be started or not. Is used for unittests. Defaults to True.
        """
        self.model = Model()
        self.view = View(self)
        self.dbstatus = False

        self.connect_to_db()
        if start_gui:
            self.view.start_gui()

    def connect_to_db(self):
        """Connect to db
            * try to establish database connection
        """
        self.dbstatus = self.model.connect_to_db()
        if self.dbstatus:
            self.view.set_status("Succesfully connected to InfluxDB")
        else:
            self.view.set_status(
                "Connection failed - Press any button to connect")

    def button_clicked(self, button):
        """Button clicked
            * this event occurs if a button is pressed
            * is called from view
            * execute action  of the button
            * try to reconnect to database if connection failed previously
        Args:
            button (str): Name of the clicked button
        """
        if self.dbstatus:
            if button == "Create - vaccine deliveries":
                self.create_vaccine_deliveries()
            if button == "Read - Germany BW vaccine deliveries":
                self.read_vaccine_deliveries_debw()
            if button == "Read - German states with most vaccines":
                self.read_states_most_vaccines()
            if button == "Read - 14d mean vaccine delivery":
                self.read_vaccine_mean()
            if button == "Read - Cumulated deliveries grouped by vaccine":
                self.read_cumulated_deliveries_by_vaccine()
            if button == "Delete - vaccine deliveries":
                self.delete_vaccine_deliveries()
            if button == "Run Unittests":
                self.run_unittest()
        else:
            self.connect_to_db()

    def create_vaccine_deliveries(self):
        """Create vaccine deliveries (only data from Germany)
            * fill database with vaccine deliveries data
            * set a status message on the gui
        """
        if self.model.create_vaccine_deliveries():
            self.view.set_status("DB is filled with vaccine delivery data")
        else:
            self.view.set_status("Could not write Vaccine delivery data to DB")

    def read_vaccine_deliveries_debw(self):
        """Read vaccine deliveries of DE-BW
            * read the data
            * set a status message to the gui
            * plot the data in a line chart
        """
        data = self.model.read_vaccine_deliveries_debw()
        if data.empty:
            self.view.set_status("Please create data first")
        else:
            self.view.set_status("Read Germany BW vaccine deliveries")
            self.view.plot_line_chart(
                data, "time", "vaccines", "Germany Baden-Wuerttemberg vaccine deliveries")

    def read_states_most_vaccines(self):
        """Read vaccine deliveries data of every state
            * read the data
            * set a status message to the gui
            * plot the data in a bar chart
        """
        data = self.model.read_states_most_vaccines()
        if data.empty:
            self.view.set_status("Please create data first")
        else:
            self.view.set_status("Read states with most vaccines")
            self.view.plot_bar_chart(
                data, "region", "vaccines", "Vaccines per state")

    def read_vaccine_mean(self):
        """Read vaccine deliveries 14 days mean
            * read the data
            * set a status message to the gui
            * plot the data in a line chart
        """
        data = self.model.read_vaccine_mean()
        if data.empty:
            self.view.set_status("Please create data first")
        else:
            self.view.set_status("Read Germany 14d mean vaccine deliveries")
            self.view.plot_line_chart(
                data, "time", "vaccines", "Germany 14d mean vaccine deliveries")

    def read_cumulated_deliveries_by_vaccine(self):
        """Read cumulated deliveries data grouped by vaccine
            * read the data
            * set a status message to the gui
            * plot the data in a line chart
        """
        data = self.model.read_cumulated_deliveries_by_vaccine()
        if data.empty:
            self.view.set_status("Please create data first")
        else:
            self.view.set_status("Read cumulated deliveries")
            self.view.plot_line_chart(
                data, "time", "vaccine", "Germany cumulated vaccine deliveries in DE-BW")

    def delete_vaccine_deliveries(self):
        """Delete vaccine deliveries data
            * delete data created by create_vaccine_deliveries()
            * set a status message to the gui
        """
        self.view.set_status("Deleting data... Please wait a moment")
        if(self.model.delete("vaccine_delivery")):
            self.view.set_status("Vaccine deliveries deleted")
        else:
            self.view.set_status("Failed to delete vaccine deliveries")
