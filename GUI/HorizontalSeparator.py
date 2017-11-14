# -*- coding: utf-8 -*-
from tkinter import *

from Model.Constants import *


class HorizontalSeparator(Frame):
    __doc__ = """Frame that represent a simple Horizontal Separator."""

    def __init__(self, parent=None, **options):
        Frame.__init__(self, parent, bg=BACKGROUND_COLOR, **options)
        separator = Frame(parent, bg=BACKGROUND_COLOR, height=2, bd=1, relief=SUNKEN)
        separator.pack(fill=X, padx=15, pady=5)
