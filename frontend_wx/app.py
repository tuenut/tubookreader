import wx

from defaults import TITLE, TITLE_PATTERN
from wx_frontend.bookview import BookView
from wx_frontend.menubar import MenuBar
from .guischemas import MENUBAR_SCHEMA


__all__ = ['MainWindow']


class MainWindow(wx.Frame):
    def __init__(self, parent, title=TITLE, *args, **kwargs):
        super().__init__(parent, title=title, size=(800, 600), *args, **kwargs)
        self.current_file_path = None

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(hbox)

        self.book_view = BookView(self)

        hbox.Add(self.book_view, 1, wx.EXPAND)

        self.__init_open_file_dialog()
        self.__init_menubar()

        self.Centre()

    def __init_menubar(self):
        self.menu_bar = MenuBar(MENUBAR_SCHEMA)
        self.SetMenuBar(self.menu_bar)
        self.Bind(wx.EVT_MENU, self.__action_open_file, self.menu_bar.File.items.open)
        self.Bind(wx.EVT_MENU, self.__action_quit, self.menu_bar.File.items.quit)

    def __init_open_file_dialog(self):
        self.open_file_dialog = wx.FileDialog(
            self, message="Open", defaultDir="", defaultFile="", wildcard="FB2 files (*.fb2)|*.fb2",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        )

    def __action_quit(self, e):
        self.Close()

    def __action_open_file(self, e):
        self.open_file_dialog.ShowModal()
        self.current_file_path = self.open_file_dialog.GetPath()
        self.__action_set_title()
        self.book_view.load(self.current_file_path)

    def __action_set_title(self):
        if self.current_file_path:
            self.SetTitle(TITLE_PATTERN % (TITLE, self.current_file_path))
        else:
            self.SetTitle(TITLE)
