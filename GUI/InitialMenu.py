# -*- coding: utf-8 -*-

from tkinter import *

from Controller.Controller import Controller
from GUI.Quitter import Quitter
from GUI.SelectionFrame import SelectionFrame
from Model.Constants import *
from Model.Model import Model


class InitialMenu(Frame):
    __doc__ = """GUI for the main menu."""

    def __init__(self, parent=None, **options):
        Frame.__init__(self, bg=BACKGROUND_COLOR, **options)
        self.title = TITLE_MENU

        self.model = Model()
        self.model.original_frame = self
        self.controller = Controller(self.model)

        self.root = parent
        self.root.protocol('WM_DELETE_WINDOW', sys.exit)
        self.root.title(TITLE_MENU)
        self.pack()

        # Label
        self.l = Label(self, text=TITLE_MENU, bg=BACKGROUND_COLOR, font=LABEL_TITLE_FONT)
        self.l.pack(side=TOP, fill=BOTH, padx=70, pady=20)

        # Manual Button
        self.create_manual_button()

        # Automatic Button
        self.create_automatic_button()

        # Button Quit
        self.create_quit_button()

    def restart(self):
        del self.model
        del self.controller

        self.model = Model()
        self.model.original_frame = self
        self.controller = Controller(self.model)

    def create_manual_button(self):
        """Create the button for the Manual Classification Phase."""
        self.b_manual = Button(self, text=MANUAL_BUTTON_TEXT, command=self.manual_callback)
        self.b_manual.config(fg='black', bg=LIGHT_GREEN, activebackground=ACTIVE_LIGHT_GREEN,
                             font=BUTTON_FONT,
                             relief=RAISED, bd=2)
        self.b_manual.pack(side=TOP, fill=BOTH, padx=70, pady=20)

    def create_automatic_button(self):
        """Create the button for the Automatic Classification Phase."""
        self.b_automatic = Button(self, text=AUTOMATIC_BUTTON_TEXT, fg='white',
                                  command=self.automatic_callback)
        self.b_automatic.config(fg='black', bg=LIGHT_BLUE, activebackground=ACTIVE_LIGHT_BLUE,
                                font=BUTTON_FONT,
                                relief=RAISED,
                                bd=2)
        self.b_automatic.pack(side=TOP, fill=BOTH, padx=70, pady=20)

    def create_quit_button(self):
        """Create the quit button with Quitter class."""
        q = Quitter(self)
        q.pack(side=TOP, fill=BOTH, padx=70, pady=(20, 40))

    def manual_callback(self):
        """Callback for the Manual Button."""
        self.hide()
        self.model.manual = True
        SelectionFrame(self.model, self.controller)

    def automatic_callback(self):
        """Callback for the Automatic Button."""
        self.hide()
        self.model.manual = False
        SelectionFrame(self.model, self.controller)

    def hide(self):
        """Hide the root Tkinter Application."""
        self.root.withdraw()

    def show(self):
        """Show the root Tkinter Application."""
        self.root.update()
        self.root.deiconify()
