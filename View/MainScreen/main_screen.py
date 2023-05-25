import os

from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivymd.toast import toast
from kivymd.uix.screen import MDScreen
from Utility.observer import Observer


class MainScreenView(MDScreen, Observer):
    controller = ObjectProperty()
    model = ObjectProperty()
    manager_screens = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.model.add_observer(self)

    def model_is_changed(self):
        pass

    def return_model(self):
        return self.model

    def return_controller(self):
        return self.controller


class SelectImagePins(Popup):
    def __init__(self, controller, model, **kwargs):
        super().__init__(**kwargs)
        self.model = model
        self.controller = controller

    def generate_file(self, num_pins, num_lines, num_thread):
        if not self.model.selected_file:
            toast("Error with the file!")
            return
        expansion = os.path.splitext(self.model.selected_file[0])[1]
        if expansion != '.png' and expansion != '.jpg':
            toast("Error with the expansion an file!")
            return
        print(self.model.selected_file)
        # generate.generate_sa(self.selected_file[0], num_pins, num_lines, num_thread)


class SelectProject(Popup):
    def __init__(self, controller, model, **kwargs):
        super().__init__(**kwargs)
        self.model = model
        self.controller = controller

    def open_project(self):
        if not self.model.selected_file:
            toast("Error with the file!")
            return
        if os.path.splitext(self.model.selected_file[0])[1] != '':
            toast("Error with the expansion an file!")
            return
        print(self.model.selected_file)


class ProgressGenerateImage(Popup):
    pass
    # def __init__(self, **kw):
    #     super(ProgressGenerateImage, self).__init__(**kw)
    #     var = self.progress_gen_image
    #     print(var)
    # def update_progress(self, dt):
    #     progress_bar = self.popup.content
    #     print(progress_bar)
    #     if progress_bar.value < progress_bar.max:
    #         progress_bar.value += dt
    #     else:
    #         self.popup.dismiss()

