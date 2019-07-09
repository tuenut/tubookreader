import json
import tkinter as tk
from utils import json_to_html


# PrettyPrinter
import pprint
pp = pprint.PrettyPrinter(indent=4, depth=10, width=140)


class BookFrame(tk.Frame):
    def __init__(self, parent, *args, bg='white', **kwargs):
        super().__init__(parent, *args, bg=bg, **kwargs)

    def __create_text_labels(self, content):
        for item in content:
            text = item['text']

            if item['subitems']:
                self.__create_text_labels(item['subitems'])

            text += item['tail']
            text_label = tk.Label(self, text=text)
            text_label.pack(side=tk.BOTTOM)

    def load_content(self, content):
        content = json.loads(content)

        for item in content:
            self.__create_text_labels(item['section'])

