from View.MainScreen.main_screen import MainScreenView


class MainScreenController:
    def __init__(self, model):
        self.model = model
        self.view = MainScreenView(controller=self, model=self.model)

    def get_view(self) -> MainScreenView:
        return self.view

    # def switch_screen(self, screen_name):
    #     self.manager_screens.current = screen_name

