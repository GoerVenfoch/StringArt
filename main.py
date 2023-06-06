from kivy import Config, platform
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from View.screens import screens


class StringArtApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_all_kv_files(self.directory)
        self.manager_screens = ScreenManager()

    def build(self):
        self.generate_application_screens()
        self.icon = "assets//window_icon//win_icon.jpg"

        if platform == 'win':
            Window.size = (400, 600)
        elif platform == 'android':
            Window.fullscreen = True

        return self.manager_screens

    def generate_application_screens(self):
        for i, name_screen in enumerate(screens.keys()):
            model = screens[name_screen]["model"]()
            controller = screens[name_screen]["controller"](model)
            view = controller.get_view()
            view.manager_screens = self.manager_screens
            view.name = name_screen
            self.manager_screens.add_widget(view)


StringArtApp().run()
