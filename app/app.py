from ui.main_window import MusicPlayerUI
from .controller import Controller
from core.player import MusicPlayer
from core.database import MusicDatabase


class App:
    def __init__(self):
        self.player = MusicPlayer()
        self.db = MusicDatabase()

        self.controller = Controller(self.player, self.db)

        # controller → UI
        self.ui = MusicPlayerUI(self.controller)

        # UI → controller
        self.controller.set_ui(self.ui)

    def run(self):
        self.ui.mainloop()
