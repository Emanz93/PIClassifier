# -*- coding: utf-8 -*-
import platform
from os import listdir, getcwd
from tkinter import *
from tkinter.messagebox import showwarning, showerror
from tkinter.simpledialog import askfloat

from GUI.HorizontalSeparator import HorizontalSeparator
from GUI.InputFrame import InputFrame
from GUI.Quitter import Quitter
from Model.Constants import *


class SelectionFrame(Toplevel):
    __doc__ = """GUI of the Manual Selection phase."""

    def __init__(self, model, controller, **other):
        # init phase
        self.model = model
        self.controller = controller

        Toplevel.__init__(self, bg=BACKGROUND_COLOR, **other)
        self.title = TITLE_INSERT
        self.protocol('WM_DELETE_WINDOW', sys.exit)
        if platform.system() != 'Darwin':
            img = PhotoImage(file=getcwd() + '/res/img/breath.png')
            self.tk.call('wm', 'iconphoto', self._w, img)

        # input frame
        self.create_input_frame()

        # button frame
        self.create_three_button()

    def create_input_frame(self):
        """Create the manual input frame in which insert the working directory."""
        self.in_frame = InputFrame(self, model=self.model, p_title=INSERT_WORKING_DIRECTORY,
                                   p_title_font=LABEL_TITLE_FONT)
        HorizontalSeparator(self)
        if not self.model.manual:  # we are in automatic.
            self.learn_frame = InputFrame(self, model=self.model, p_title=INSERT_LEARN_DIRECTORY,
                                          p_title_font=LABEL_TITLE_FONT)
            HorizontalSeparator(self)
            self.create_sesibility_panel()
            HorizontalSeparator(self)

    def create_sesibility_panel(self):
        """Build the sensibility panel, that give the ability to fix the sensibility value for the automatic classifier."""
        f = Frame(self)
        f.config(bg=BACKGROUND_COLOR, height=75, width=FRAME_SELECT_WIDTH, padx=10, pady=10)
        f.pack_propagate(0)
        f.pack(side=TOP)

        self.sensib_label = Label(f, text=SENSIBILITY_LABEL, bg=BACKGROUND_COLOR, font=LABEL_DESCRIPTION_FONT)
        self.sensib_label.pack(side=LEFT)
        self.sensib_label_val = Label(f, text=self.model.settings['sensibility'], bg=BACKGROUND_COLOR,
                                      font=LABEL_DESCRIPTION_FONT)
        self.sensib_label_val.pack(side=LEFT)
        self.sensib_button = Button(f, text="Imposta", font=BUTTON_FONT, relief=RAISED, bd=2,
                                    command=self.sensib_callback)
        self.sensib_button.pack(side=RIGHT)

    def create_three_button(self):
        """Create the bottom panel and fill it with the navigations buttons."""
        f = Frame(self)
        f.config(bg=BACKGROUND_COLOR, height=75, width=FRAME_SELECT_WIDTH, padx=10, pady=10)
        f.pack_propagate(0)
        f.pack(side=TOP, expand=False)

        # Quitter button
        Quitter(f).pack(side=LEFT)
        # Back Button
        Button(f, text="Indietro", font=BUTTON_FONT, relief=RAISED, bd=2,
               command=self.back_callback).pack(side=LEFT)
        # Next Button
        Button(f, text="Avanti", font=BUTTON_FONT, relief=RAISED, bd=2,
               command=self.next_callback).pack(side=RIGHT)
        self.bind('<Return>', (lambda event: self.next_callback()))

    def next_callback(self):
        """Callback of the next button. Launch the ManualController. It will start the next view."""
        if self.model.settings['working_directory_path'] is None:
            showwarning("Attenzione", "Selezionare la directory di lavoro.")
        elif self.model.settings['knowledge_base_path'] is None:
            showwarning("Attenzione", "Selezionare la directory della Knowledge Base.")
        else:
            if self.controller.check_valid_wd() and self.controller.check_valid_ld():
                # call the controller. It will have different behaviour with different self.model.manual's value.
                if self.controller.choose_work():
                    self.controller.start()
                    self.destroy()

    def back_callback(self):
        """Callback ofthe previous button."""
        self.model.original_frame.show()
        self.destroy()

    def sensib_callback(self):
        """Callback for the button to fix the sensibilation level. It open a new popup asking a float."""
        res = askfloat(ASKSENSIB_TITLE, ASKSENSIB_MESSAGE,
                       initialvalue=self.model.settings['sensibility'], minvalue=0.0, maxvalue=1.0)
        if res is not None:
            self.model.settings['sensibility'] = res
            self.sensib_label_val.config(text=self.model.settings['sensibility'])
