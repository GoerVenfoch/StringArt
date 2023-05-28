from View.ViewInstuctionScreen.view_instuction_screen import ViewInstructionScreenView


class ViewInstructionScreenController:
    def __init__(self, model):
        self.model = model
        self.view = ViewInstructionScreenView(controller=self, model=self.model)

    def get_view(self) -> ViewInstructionScreenView:
        return self.view

    def switch_screen(self, screen_name):
        self.view.manager_screens.current = screen_name
