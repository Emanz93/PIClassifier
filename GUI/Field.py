# -*- coding: utf-8 -*-
from tkinter import *

from Model.Constants import BACKGROUND_COLOR


class Field(Frame):
    __doc__ = """Class for the creation Field. This is a Frame with a Label on the left side, and a
    Entry on the right side."""

    def __init__(self, parent=None, label=None, entry="", **options):
        Frame.__init__(self, parent, bg=BACKGROUND_COLOR, **options)
        left = Frame(self, bg=BACKGROUND_COLOR)
        right = Frame(self, bg=BACKGROUND_COLOR)
        self.pack(fill=X)
        left.pack(side=LEFT, )
        right.pack(side=RIGHT, expand=YES, fill=X)

        lab = Label(left, bg=BACKGROUND_COLOR, width=8, text=label)
        self.ent = Entry(right)

        self.var = StringVar()
        self.var.set(str(entry))
        self.ent.config(textvariable=self.var)

        lab.pack(side=TOP)
        self.ent.pack(side=TOP, fill=X)

    def get_variable(self):
        """Get the variable inside the Entry."""
        return self.var

    def set_variable(self, s):
        """Set the model's variable of the Entry. Use this to update automatically the field's
        view."""
        self.var.set(str(s))
