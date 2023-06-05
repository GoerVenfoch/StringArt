from View.ViewStrArtScreen.view_str_art_screen import ViewStrArtScreenView


class ViewStrArtScreenController:
    def __init__(self, model):
        self.model = model
        self.view = ViewStrArtScreenView(controller=self, model=self.model)

    def get_view(self) -> ViewStrArtScreenView:
        return self.view

    def switch_screen(self, screen_name):
        self.view.manager_screens.current = screen_name
