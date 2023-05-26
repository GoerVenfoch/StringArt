from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen

from Utility.subject import Subject
from Utility.observer import Observer


class ViewStrArtScreenView(MDScreen, Observer):
    controller = ObjectProperty()
    model = ObjectProperty()
    manager_screens = ObjectProperty()
    subject = Subject()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.subject.attach(self)

    def on_enter(self):
        print(self.model.selected_file)

    def update(self, subject: Subject):
        if subject._path_file != "":
            self.model.selected_file = subject._path_file
