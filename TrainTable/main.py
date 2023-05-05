from kivy.config import Config

from controller import Controller
from view import View

Config.set("graphics", "width", 1250)
Config.set("graphics", "height", 1000)

from kivymd.app import MDApp

class MyApp(MDApp):
    title = 'Таблица рейсов'

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        view = View()
        view.set_app(self)
        controller = Controller()
        controller.set_app(self)
        return view.update_frame(self, controller.get_trips())

if __name__ == '__main__':
    MyApp().run()
