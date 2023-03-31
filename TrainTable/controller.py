from model import Model
from view import View


class Controller:
    def __init__(self, App):
        self.app = App
    model = Model()
    view = View()

    def start_build(self):
        return self.view.update_frame(self.app, self.model.get_trips())

    def add_trip(self):

        self.model.add_trip(self.app)

    def remove_trip(self):
        self.model.remove_trip(self.app)
