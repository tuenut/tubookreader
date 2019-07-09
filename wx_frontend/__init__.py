from wx import App
from .app import MainWindow


class Application(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_window = MainWindow(parent=None, *args, **kwargs)
        self.main_window.Show()
        self.MainLoop()
