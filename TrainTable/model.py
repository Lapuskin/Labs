from view import View


class Model:
    trips = [
       # '1', 'Нарния', 'Средиземье', '11.11 11:01:2011','11.11 11:11:2011', '10 минут'
    ]
    view = View()

    def add_trip(self, trip, app):
        self.trips.append(trip)
        self.view.update_frame(app, self.trips)

    def remove_trip(self, trip, app):
        self.trips.remove(trip)
        self.view.update_frame(app, self.trips)

    def get_trips(self):
        return self.trips
