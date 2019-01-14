# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.messagebox import askokcancel

from Model.Constants import *

from sys import platform


class Quitter(Button):
    __doc__ = """A Quit button that verifies exit requests."""

    def __init__(self, parent=None, **options):
        Button.__init__(self, parent, **options)
        self.pack()
        self.config(text='Esci', command=self.quit)
        self.config(fg='black', bg=LIGHT_RED, activebackground=ACTIVE_LIGHT_RED, font=BUTTON_FONT,
                    relief=RAISED, bd=2)

        if platform == "darwin": # MAC OS
            self.config(highlightbackground=LIGHT_RED)

    def quit(self):
        """Override of the superclass' method quit."""
        ans = askokcancel('Esci', 'Vuoi veramente uscire?')
        if ans:
            sys.exit()
