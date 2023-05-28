from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen
from Utility.observer import Observer
from Utility.subject import Subject


class ViewInstructionScreenView(MDScreen, Observer):
    controller = ObjectProperty()
    model = ObjectProperty()
    manager_screens = ObjectProperty()
    subject = Subject()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.subject.attach(self)

    def on_enter(self):
        pass
