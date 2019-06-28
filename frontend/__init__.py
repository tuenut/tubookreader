import wx

from .app import MainWindow


def start_gui(*args, **kwargs):
    application = wx.App()
    main_window = MainWindow(parent=None, *args, **kwargs)
    main_window.Show()
    application.MainLoop()