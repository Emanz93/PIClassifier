# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.filedialog import askdirectory

from GUI.Field import Field
from Model.Constants import *

from sys import platform

class InputFrame(Frame):
    __doc__ = """Manual Input Frame. Contain a Label that is the title of the section, a Field and a
    Button."""

    def __init__(self, parent, model=None, p_title=None, p_title_font=None,
                 **options):
        Frame.__init__(self, parent, bg=BACKGROUND_COLOR, **options)

        # model
        self.model = model

        # parent frame
        self.f = Frame(parent, bg=BACKGROUND_COLOR)
        self.f.config(height=FRAME_SELECT_HEIGHT, width=FRAME_SELECT_WIDTH, padx=10, pady=10)
        self.f.pack_propagate(0)
        self.f.pack(side=TOP, expand=False)

        Label(self.f, bg=BACKGROUND_COLOR, text=p_title, font=p_title_font).pack(side=TOP)

        self.inputFrame = Frame(self.f, bg=BACKGROUND_COLOR, height=15, width=FRAME_SELECT_WIDTH)

        self.b_photo = PhotoImage(file="./res/img/openfile.gif", width="15", height="15")

        # check if it is manual or automatic.
        if p_title == INSERT_WORKING_DIRECTORY:
            self.field = Field(self.inputFrame, label='Directory', entry=self.model.settings['working_directory_path'])
            self.selectButton = Button(self.inputFrame, image=self.b_photo, width="15", height="15",
                                       command=self.ask_working_directory_callback)
        else:
            self.field = Field(self.inputFrame, label='Directory', entry=self.model.settings['knowledge_base_path'])
            self.selectButton = Button(self.inputFrame, image=self.b_photo, width="15", height="15",
                                       command=self.ask_learning_directory_callback)
        self.field.pack(fill=X, side=LEFT)
        self.selectButton.pack(side=RIGHT)

        self.inputFrame.pack(side=BOTTOM, expand=False)

        if platform == "darwin": # MAC OS
            self.f.config(highlightbackground=BACKGROUND_COLOR)
            self.inputFrame.config(highlightbackground=BACKGROUND_COLOR)

    def ask_working_directory_callback(self):
        """Callback of the button. Ask a directory via file dialog. Store the path in the model and
        update the field."""
        try:
            self.model.settings['working_directory_path'] = askdirectory(title="Selezionare la directory di lavoro:",
                               initialdir=self.model.settings['working_directory_path'])  + "/"
            self.field.set_variable(self.model.settings['working_directory_path'])
        except TypeError:
            return

    def ask_learning_directory_callback(self):
        """Callback of the button. Ask a directory via file dialog. Store the path in the model and
        update the field."""
        try:
            self.model.settings['knowledge_base_path'] = askdirectory(title="Selezionare la directory contentente la Knowledge Base:",
                               initialdir=self.model.settings['knowledge_base_path']) + "/"
            self.field.set_variable(self.model.settings['knowledge_base_path'])
        except TypeError:
            return
