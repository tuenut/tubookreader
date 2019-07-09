import tkinter as tk

from tk_frontend.bookframe import BookFrame
from backend import FB2Book
from locals import TEST_BOOK


class Application(tk.Tk):
    def __init__(self, title=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(title)
        self.geometry("%sx%s" % (800, 600))

        frame = tk.Frame(self, bg='grey', border=4, relief=tk.FLAT)
        frame.pack(expand=True, fill=tk.BOTH)

        # self.content_frame = tk.Frame(frame, bg='grey77')
        # self.content_frame.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

        self.book_frame = BookFrame(parent=frame)
        self.book_frame.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

        self.book = FB2Book(TEST_BOOK)
        self.book_frame.load_content(self.book.body.get_sections())

        self.mainloop()


