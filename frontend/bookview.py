import wx

from backend import FB2Book


class BookView(wx.Panel):
    FLAG = 0
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.SetBackgroundColour('#005500')

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(hbox)

        self.splitter = wx.SplitterWindow(self, wx.SPLIT_VERTICAL, style=wx.SP_BORDER|wx.SP_LIVE_UPDATE, size=(100,-1))
        self.splitter.SetMinimumPaneSize(200)
        self.splitter.FitInside()

        self.__init_table_of_contents()
        self.__init_book_view()

        self.splitter.SplitVertically(self.table_of_contents, self.book_content)

        hbox.Add(self.splitter, wx.ID_ANY, flag=wx.EXPAND | wx.ALL)

        self.book = FB2Book()

    def load(self, file_path):
        self.book.load(file_path)

        table_of_contantes = '\n'.join(i[0] for i in self.book.body.table_of_contents)
        print(table_of_contantes)
        self.table_of_contents_text.SetLabelText(table_of_contantes)

    def __init_book_view(self):
        self.book_content = wx.ScrolledWindow(self.splitter, wx.ID_ANY,)
        self.book_content.SetScrollbars(1, 1, 1, 1)
        self.book_content.SetBackgroundColour('#999999')

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.book_content.SetSizer(hbox)

        self.book_content_text = wx.StaticText(self.book_content, label='Book content', style=wx.ALIGN_LEFT)
        self.book_content_text.SetFont(wx.Font())

        hbox.Add(self.book_content_text, 1)

    def __init_table_of_contents(self):
        self.table_of_contents = wx.ScrolledWindow(self.splitter, wx.ID_ANY)
        self.table_of_contents.SetScrollbars(1, 1, 1, 1)
        self.table_of_contents.SetBackgroundColour('#ffffff')

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.table_of_contents.SetSizer(hbox)

        self.table_of_contents_text = wx.StaticText(self.table_of_contents, label='Table of contents', style=wx.ALIGN_LEFT)
        self.table_of_contents_text.SetFont(wx.Font())

        hbox.Add(self.table_of_contents_text, 1)