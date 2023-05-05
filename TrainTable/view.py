from controller import Controller

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from kivymd.uix.datatables import MDDataTable
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from kivy.metrics import dp


class View:
    controller = Controller()

    class MyPopup(Popup):
        def __init__(self):
            add_popup_layout = BoxLayout(orientation='vertical', spacing='10')
            input_departure = TextInput()
            input_arrival = TextInput()
            input_date_departure = TextInput()
            input_date_arrival = TextInput()
            submit_button = Button(text='Добавить')
            submit_button.bind(on_press=self.send_trip)
            add_popup_layout.add_widget(Label(text='Введите станцию отправления'))
            add_popup_layout.add_widget(input_departure)
            add_popup_layout.add_widget(Label(text='Введите станцию прибытия'))
            add_popup_layout.add_widget(input_arrival)
            add_popup_layout.add_widget(Label(text='Введите дату и время отправления'))
            add_popup_layout.add_widget(input_date_departure)
            add_popup_layout.add_widget(Label(text='Введите дату и время прибытия'))
            add_popup_layout.add_widget(input_date_arrival)
            add_popup_layout.add_widget(submit_button)
            popup = Popup(title='Добавить рейс', content=add_popup_layout, size_hint=(None, None), size=(300, 450))
            popup.open()

    def set_app(self, App):
        self.app = App

    def send_trip(self, instance):
        trip = []
        trip.append(self.input_departure)
        trip.append(self.input_arrival)
        trip.append(self.input_date_departure)
        trip.append(self.input_date_arrival)
        self.controller.add_trip(trip)
        self.update_frame(self.controller.get_app())

    def add_trip(self, instance):

    def update_frame(self, app, trips):
        self.controller.set_app(self.app)
        layout = RelativeLayout()
        app.data_tables = MDDataTable(
            size_hint=(0.8, 0.8),
            pos=(100, 100),
            use_pagination=True,
            check=True,
            column_data=[
                ("Номер", dp(30), None, "Custom tooltip"),
                ("Отправление", dp(30)),
                ("Прибытие", dp(30)),
                ("Время отправления", dp(30)),
                ("Время прибытия", dp(30)),
                ("Время в пути", dp(30))
            ],
            row_data=trips
        )
        adding_button = Button(text='Добавить рейс',
                               size_hint=(.2, .1),
                               pos=(0, 0)
                               )

        remove_button = Button(text='Удалить рейс',
                               size_hint=(.2, .1),
                               pos=(640, 0)
                               )

        adding_button.bind(on_press=self.add_trip)

        layout.add_widget(app.data_tables)
        layout.add_widget(adding_button)
        layout.add_widget(remove_button)
        return layout
