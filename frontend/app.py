import wx
import json

from backend import FB2Book
from utils import get_instance_vals


class MainWindow(wx.Frame):
    TITLE = 'TubookReader'
    def __init__(self, parent, title=TITLE, *args, **kwargs):
        self.current_file_path = None
        self.book = None

        super().__init__(parent, title=title, size=(350, 300), *args, **kwargs)

        self.open_file_dialog = wx.FileDialog(self, "Open", "", "", "Python files (*.fb2)|*.fb2",
                                              wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)


        self.__init_menubar()
        self.__init_book_view()

        self.Centre()

    def __init_menubar(self):
        menubar = wx.MenuBar()

        menu_file = wx.Menu()

        file_item_open = menu_file.Append(wx.ID_OPEN, '&Open')
        menu_file.AppendSeparator()
        file_item_quit = menu_file.Append(wx.ID_EXIT, 'Quit', 'Quit application')

        menubar.Append(menu_file, '&File')

        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.action_open_file, file_item_open)
        self.Bind(wx.EVT_MENU, self.action_quit, file_item_quit)

    def __init_book_view(self):
        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        font = wx.Font()

        self.text = wx.StaticText(pnl, label='', style=wx.ALIGN_LEFT)

        self.text.SetFont(font)

        vbox.Add(self.text, flag=wx.ALL, border=15)

        pnl.SetSizer(vbox)

    def action_quit(self, e):
        self.Close()

    def action_open_file(self, e):
        self.open_file_dialog.ShowModal()

        self.current_file_path = self.open_file_dialog.GetPath()

        self.action_set_title()

        if self.current_file_path:
            self.render_book()

    def action_set_title(self):
        self.SetTitle('%s [%s]' % (self.TITLE, self.current_file_path))

    def render_book(self):
        self.book = FB2Book(self.current_file_path)

        self.text.SetLabelText('\n'.join(i[0] for i in self.book.body.table_of_contents))




