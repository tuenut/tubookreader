import wx

MENUBAR_SCHEMA = {
    'File': (
        {'name': 'open', 'args': (wx.ID_OPEN, '&Open')},
        {'name': None},
        {'name': 'quit', 'args': (wx.ID_EXIT, 'Quit', 'Quit application')},
    )
}