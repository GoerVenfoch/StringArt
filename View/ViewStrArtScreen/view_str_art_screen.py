import ast
import math

from kivy.graphics import Color, Point, Ellipse
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
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
        # self.current_canvas = self.ids.widget_canvas

    def on_enter(self):
        self.read_file()
        self.ids.container.add_widget(StringArtPreview(self.model.num_points))

    def update(self, subject: Subject):
        if subject._path_file != "":
            self.model.selected_file = subject._path_file

    def read_file(self):
        with open(self.model.selected_file, 'r') as file:
            line = file.readline()
            parts = line.split('.')
            self.model.num_points = int(parts[0].strip())
            self.model.list_inst = ast.literal_eval(parts[1].strip())


class StringArtPreview(Widget):
    def __init__(self, num, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update, size=self.update)
        self.num_points = num

    def update(self, *args):
        self.canvas.clear()
        angle = 2 * math.pi / self.num_points
        radius = min(self.width, self.height) / 2 - 1

        with self.canvas:
            Color(1 / 255, 1 / 255, 1 / 255)
            for i in range(self.num_points):
                x = int(radius * math.cos(i * angle))
                y = int(radius * math.sin(i * angle))
                Ellipse(pos=(self.center_x + x - 1, self.center_y + y - 1), size=(3, 3))
