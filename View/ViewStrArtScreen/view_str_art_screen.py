from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen
from Utility.observer import Observer


class ViewStrArtScreenView(MDScreen, Observer):
    controller = ObjectProperty()
    model = ObjectProperty()
    manager_screens = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.model.add_observer(self)

    def model_is_changed(self):
        pass
