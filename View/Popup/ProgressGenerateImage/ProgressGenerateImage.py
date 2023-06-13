from kivy.uix.popup import Popup
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.progressbar import MDProgressBar


class ProgressGenerateImage(Popup):
    def __init__(self, max_value, **kw):
        super(ProgressGenerateImage, self).__init__(**kw)
        self.progress_bar = self.ids.progress_bar_id
        self.progress_bar.max = max_value

    def update_progress(self, dt):
        if self.progress_bar.value < self.progress_bar.max:
            self.progress_bar.value += dt
        else:
            self.ids.next_progress_id.disabled = False
