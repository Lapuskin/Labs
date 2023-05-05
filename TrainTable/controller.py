from model import Model


class Controller:
    def set_app(self, App):
        self.app = App

    def get_app(self):
        return self.app

    model = Model()

    def get_trips(self):
        return self.model.trips

    def start_build(self):
        return self.view.update_frame(self.app, self.model.get_trips())

    def add_trip(self, trip):
        self.model.add_trip(trip)

    def remove_trip(self):
        self.model.remove_trip(self.app)
