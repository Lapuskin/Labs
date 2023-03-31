from kivy.config import Config

from controller import Controller

Config.set("graphics", "width", 1250)
Config.set("graphics", "height", 1000)

from kivymd.app import MDApp

class MyApp(MDApp):
    title = 'Таблица рейсов'

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        controller = Controller(self)
        return controller.start_build()


if __name__ == '__main__':
    MyApp().run()
