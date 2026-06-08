from ui.main_window import MusicPlayerUI
from app.dummy_controller import DummyController

app = MusicPlayerUI(DummyController())
app.mainloop()