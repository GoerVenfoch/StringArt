import threading
import os

from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivymd.toast import toast
from kivymd.uix.screen import MDScreen

from Utility import generate
from Utility.observer import Observer
from Utility.subject import Subject
from View.Popup.ProgressGenerateImage.ProgressGenerateImage import ProgressGenerateImage


class MainScreenView(MDScreen, Observer):
    controller = ObjectProperty()
    model = ObjectProperty()
    manager_screens = ObjectProperty()
    subject = Subject()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.subject.attach(self)

    def update(self, subject):
        if subject._path_file != "":
            self.model.selected_file = subject._path_file

    def return_model(self):
        return self.model

    def return_controller(self):
        return self.controller


# async def async_generate_sa(controller, selected_file, num_pins, num_lines, num_thread):
#     await asyncio.sleep(0)
#     toast("jjjj")
#     generate.generate_sa(selected_file, num_pins, num_lines, num_thread)
#     controller.switch_screen('view screen')


class SelectImagePins(Popup, Observer):
    subject = Subject()

    def __init__(self, controller, model, **kwargs):
        super().__init__(**kwargs)
        self.model = model
        self.controller = controller
        self.subject.attach(self)

    def generate_file(self, num_pins, num_lines, num_thread):
        if not self.model.selected_file:
            toast("Error with the file!")
            return
        expansion = os.path.splitext(self.model.selected_file)[1]
        if expansion != '.png' and expansion != '.jpg':
            toast("Error with the expansion an file!")
            return

        progress_popup = ProgressGenerateImage(num_lines + 1)
        progress_popup.bind(on_dismiss=self.next_after_generate_image)
        progress_popup.open()
        threading.Thread(target=generate.generate_sa,
                         args=(self.model.selected_file,
                               num_pins,
                               num_lines,
                               num_thread,
                               progress_popup)).start()
        self.dismiss()

    def next_after_generate_image(self, instance):
        self.subject.put_data(os.path.splitext(os.path.basename(self.model.selected_file))[0],
                              self.model.num_points,
                              self.model.list_inst)
        self.subject.detach(self)
        self.controller.switch_screen('view screen')


class SelectProject(Popup, Observer):
    subject = Subject()

    def __init__(self, controller, model, **kwargs):
        super().__init__(**kwargs)
        self.model = model
        self.controller = controller
        self.subject.attach(self)

    def open_project(self):
        if not self.model.selected_file:
            toast("Error with the file!")
            return
        if os.path.splitext(self.model.selected_file)[1] != '':
            toast("Error with the expansion an file!")
            return
        self.subject.put_data(self.model.selected_file, self.model.num_points, self.model.list_inst)
        self.subject.detach(self)
        self.controller.switch_screen('view screen')
