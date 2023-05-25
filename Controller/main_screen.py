from View.MainScreen.main_screen import MainScreenView


class MainScreenController:
    def __init__(self, model):
        self.model = model  # Model.slider_menu_screen.SliderMenuScreenModel
        self.view = MainScreenView(controller=self, model=self.model)

    def get_view(self) -> MainScreenView:
        return self.view
