from View.ViewStrArtScreen.view_str_art_screen import ViewStrArtScreenView


class ViewStrArtScreenController:
    def __init__(self, model):
        self.model = model  # Model.slider_menu_screen.SliderMenuScreenModel
        self.view = ViewStrArtScreenView(controller=self, model=self.model)

    def get_view(self) -> ViewStrArtScreenView:
        return self.view