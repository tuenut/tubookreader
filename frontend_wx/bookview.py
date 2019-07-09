import wx
import json

from backend import FB2Book


class BookView(wx.Panel):
    FLAG = 0

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.book_content = None

        self.SetBackgroundColour('#005500')

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(hbox)

        self.__init_table_of_contents()
        # self.__init_book_view()

        hbox.Add(self.table_of_contents, wx.ID_ANY, flag=wx.EXPAND | wx.ALL)

        self.book = FB2Book()

    def load(self, file_path):
        self.book.load(file_path)

        self.book_content = json.loads(self.book.body.get_sections())

        for item in self.book_content:
            table_of_contents_text = wx.StaticText(self.table_of_contents, label=str(item['title']),
                                                   style=wx.ALIGN_LEFT)
            table_of_contents_text.SetFont(wx.Font())

            self.table_of_contents_vbox.Add(table_of_contents_text, wx.ID_ANY,)

    def __init_book_view(self):
        self.book_content = wx.ScrolledWindow(self, wx.ID_ANY,)
        self.book_content.SetScrollbars(1, 1, 1, 1)
        self.book_content.SetBackgroundColour('#999999')

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.book_content.SetSizer(hbox)

        self.book_content_text = wx.StaticText(self.book_content, label='Book content', style=wx.ALIGN_LEFT)
        self.book_content_text.SetFont(wx.Font())

        hbox.Add(self.book_content_text, 1)

    def __init_table_of_contents(self):
        self.table_of_contents = wx.ScrolledWindow(self, wx.ID_ANY)
        self.table_of_contents.SetScrollbars(1, 1, 1, 1)
        self.table_of_contents.SetBackgroundColour('#ffffff')

        self.table_of_contents_vbox = wx.BoxSizer(wx.VERTICAL)
        self.table_of_contents.SetSizer(self.table_of_contents_vbox)
