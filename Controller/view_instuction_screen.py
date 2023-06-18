from kivy.clock import Clock

from View.ViewInstuctionScreen.view_instuction_screen import ViewInstructionScreenView


class ViewInstructionScreenController:
    def __init__(self, model):
        self.model = model
        self.view = ViewInstructionScreenView(controller=self, model=self.model)

    def get_view(self) -> ViewInstructionScreenView:
        return self.view

    def switch_screen(self, screen_name):
        self.clear_screen()
        self.view.manager_screens.current = screen_name

    def clear_screen(self):
        Clock.unschedule(self.view.read_list_inst)
        self.model.buffer_outlist = [''] * self.model.size_list_buffer_outlist
        self.model.current_ind_list = 0
        self.model.is_paused = None
        self.model.schedule_interval = 6

    def set_pause(self):
        self.view.toggle_play_pause()
