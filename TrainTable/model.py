from datetime import datetime

class Model:
    trips = [
        (1, 'Нарния', 'Средиземье', '2020-02-12 13:20:10', '2020-02-12 13:50:10', '12')
    ]

    def add_trip(self, trip):
        trip.insert(0, len(self.trips) + 1)
        trip[3] = datetime.strptime(trip[3].text, '%Y-%m-%d %H:%M:%S')
        trip[4] = datetime.strptime(trip[4].text, '%Y-%m-%d %H:%M:%S')
        trip.append(trip[4] - trip[3])
        self.trips.append(tuple(trip))

    def remove_trip(self, trip, app):
        self.trips.remove(trip)
        self.view.update_frame(app, self.trips)

    def get_trips(self):
        return self.trips
