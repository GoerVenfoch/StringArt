from Controller.main_screen import MainScreenController
from Controller.view_instuction_screen import ViewInstructionScreenController
from Controller.view_str_art_screen import ViewStrArtScreenController
from Model.main_screen import MainScreenModel
from Model.view_instuction_screen import ViewInstructionScreenModel
from Model.view_str_art_screen import ViewStrArtScreenModel

screens = {
    "main screen": {
        "model": MainScreenModel,
        "controller": MainScreenController,
    },
    "view screen": {
        "model": ViewStrArtScreenModel,
        "controller": ViewStrArtScreenController,
    },
    "view instruction": {
        "model": ViewInstructionScreenModel,
        "controller": ViewInstructionScreenController,
    },
}
