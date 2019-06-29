import wx


class MenuBar(wx.MenuBar):
    def __init__(self, menu_schema, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for item in menu_schema:
            setattr(self, item, self.CustomMenu(menu_schema[item]))
            self.Append(getattr(self, item), '&%s' % item)

    class CustomMenu(wx.Menu):
        def __init__(self, menu_items: list or tuple, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.items = type('MenuItems', (object,), dict())

            for item in menu_items:
                if item['name']:
                    setattr(self.items, item['name'], self.Append(*item['args']))
                else:
                    self.AppendSeparator()