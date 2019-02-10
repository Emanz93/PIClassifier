# -*- coding: utf-8 -*-
from os import getcwd
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showwarning, askyesno

from Controller.Processer import Processer
from GUI.Field import *
from GUI.Quitter import Quitter
from Model.Constants import *

from sys import platform


class ResultFrame(Toplevel):
    __doc__ = """GUI for the Manual Classification phase."""

    def __init__(self, model, controller, **options):
        Toplevel.__init__(self, bg=BACKGROUND_COLOR, **options)
        self.title = TITLE_CLASSIFICATION
        self.protocol('WM_DELETE_WINDOW', self.quit)
        #img = PhotoImage(file=getcwd() + '/res/img/breath.png')
        #self.tk.call('wm', 'iconphoto', self._w, img)

        # model
        self.model = model
        # controller
        self.controller = controller

        # creating the view
        self.create_parents_panels()
        self.create_top_left_panel()
        if self.model.manual is False:  # Automatic Case
            self.create_top_central_panel()
            self.create_top_right_panel()

            if platform == "darwin": #MAC OS
                self.central_panel.config(highlightbackground=BACKGROUND_COLOR)
                self.top_right_frame.config(highlightbackground=BACKGROUND_COLOR)
                self.ck_anomaly.config(highlightbackground=BACKGROUND_COLOR)
                self.ck_ok.config(highlightbackground=BACKGROUND_COLOR)
                self.ck_dubious.config(highlightbackground=BACKGROUND_COLOR)
                self.set_button.config(highlightbackground=LIGHT_BLUE)

        self.create_bottom_panel()

        self.controller.save_json_settings()

        if platform == "darwin": # MAC OS
            self.parent1.config(highlightbackground=BACKGROUND_COLOR)
            self.parent2.config(highlightbackground=BACKGROUND_COLOR)
            self.top_left_frame.config(highlightbackground=BACKGROUND_COLOR)
            self.bottom_frame.config(highlightbackground=BACKGROUND_COLOR)
            self.top_bottom_frame.config(highlightbackground=BACKGROUND_COLOR)
            self.dataset_button.config(highlightbackground=LIGHT_VIOLET)
            self.bottom_bottom_frame.config(highlightbackground=BACKGROUND_COLOR)
            self.menu_button.config(highlightbackground=LIGHT_GREEN)

    def create_parents_panels(self):
        """Create two parents panel. Parent1 is the main top frame. Parent2 is the bottom frame."""
        self.parent1 = Frame(self, bg=BACKGROUND_COLOR, height=FRAME_RESULT_HEIGHT * 2 / 3,
                             width=FRAME_RESULT_WIDTH, padx=30, pady=30)
        self.parent1.pack(side=TOP)
        self.parent2 = Frame(self, bg=BACKGROUND_COLOR, height=FRAME_RESULT_HEIGHT * 1 / 3,
                             width=FRAME_RESULT_WIDTH, padx=30, pady=30)
        self.parent2.pack(side=BOTTOM)

    def create_top_left_panel(self):
        """Create the top left frame. Contains the classification result in a set of Fields."""
        self.top_left_frame = Frame(self.parent1, bg=BACKGROUND_COLOR, padx=10)
        self.top_left_frame.pack(side=LEFT)

        # title
        Label(self.top_left_frame, bg=BACKGROUND_COLOR, text='Risultati', font=LABEL_TITLE_FONT).pack()

        # Fields
        self.anomaly_field = Field(self.top_left_frame, label='Anomale',
                                   entry=self.model.anomaly_counter, pady=9)
        self.anomaly_field.pack()
        self.ok_field = Field(self.top_left_frame, label='OK', entry=self.model.ok_counter,
                              pady=9)
        self.ok_field.pack()
        if self.model.manual is False:
            self.dubious_field = Field(self.top_left_frame, label='Dubbie',
                                       entry=self.model.dubious_counter, pady=9)
            self.dubious_field.pack()

    def create_top_central_panel(self):
        """Create the top central frame. Contains the check boxes."""
        self.central_panel = Frame(self.parent1, bg=BACKGROUND_COLOR, padx=10, width=FRAME_RESULT_WIDTH)
        self.central_panel.pack(side=LEFT)

        # title
        Label(self.central_panel, bg=BACKGROUND_COLOR, text='Modifica', font=LABEL_TITLE_FONT).pack()

        # Check buttons
        for i in range(3):
            self.model.check_vars.append(IntVar(0))

        self.ck_anomaly = Checkbutton(self.central_panel, pady=10, text='Anomale',
                                      variable=self.model.check_vars[0], bg=BACKGROUND_COLOR)
        if int(self.anomaly_field.get_variable().get()) == 0:
            self.ck_anomaly.config(state=DISABLED)
        self.ck_anomaly.pack()

        self.ck_ok = Checkbutton(self.central_panel, pady=10, text='  Ok   ',
                                 variable=self.model.check_vars[1], bg=BACKGROUND_COLOR)
        if int(self.ok_field.get_variable().get()) == 0:
            self.ck_ok.config(state=DISABLED)
        self.ck_ok.pack()

        self.ck_dubious = Checkbutton(self.central_panel, pady=10, text='Dubbie',
                                      variable=self.model.check_vars[2], bg=BACKGROUND_COLOR)
        if int(self.dubious_field.get_variable().get()) == 0:
            self.ck_dubious.config(state=DISABLED)
        self.ck_dubious.pack()

    def create_top_right_panel(self):
        """Create the top right panel containing the check boxes."""
        self.top_right_frame = Frame(self.parent1, bg=BACKGROUND_COLOR, padx=10)
        self.top_right_frame.pack(side=LEFT)

        self.set_button = Button(self.top_right_frame, text=VERIFY_BUTTON_TEXT, fg='black',
                                 bg=LIGHT_BLUE, activebackground=ACTIVE_LIGHT_BLUE,
                                 font=BUTTON_FONT, relief=RAISED, bd=2,
                                 command=self.verify_callback)
        self.set_button.pack()

    def create_bottom_panel(self):
        """Create the bottom panel containing the Exit and Menu button."""
        self.bottom_frame = Frame(self.parent2, bg=BACKGROUND_COLOR, width=FRAME_RESULT_WIDTH, padx=10)
        self.bottom_frame.pack(side=BOTTOM)

        self.top_bottom_frame = Frame(self.bottom_frame, bg=BACKGROUND_COLOR, width=FRAME_RESULT_HEIGHT,
                                      padx=10)
        self.top_bottom_frame.pack(side=TOP)

        self.dataset_button = Button(self.top_bottom_frame, text=DATASET_BUTTON_TEXT)
        self.dataset_button.config(fg='black', bg=LIGHT_VIOLET,
                                   activebackground=ACTIVE_LIGHT_VIOLET,
                                   font=BUTTON_FONT, relief=RAISED, bd=2,
                                   command=self.dataset_callback)
        self.dataset_button.pack()

        self.bottom_bottom_frame = Frame(self.bottom_frame, bg=BACKGROUND_COLOR, width=FRAME_RESULT_HEIGHT,
                                         padx=10)
        self.bottom_bottom_frame.pack(side=BOTTOM)

        self.menu_button = Button(self.bottom_bottom_frame, text=MENU_BUTTON_TEXT)
        self.menu_button.config(fg='black', bg=LIGHT_GREEN, activebackground=ACTIVE_LIGHT_GREEN,
                                font=BUTTON_FONT, relief=RAISED, bd=2, command=self.menu_callback)
        self.menu_button.pack(side=LEFT)
        self.quit_button = Quitter(self.bottom_bottom_frame)

    def menu_callback(self):
        """Callback of the Menu button. Show the menu screen."""
        self.model.original_frame.show()
        self.model.original_frame.restart()
        self.destroy()

    def verify_callback(self):
        """Start the manual classification mode on the curve selected by the check box."""
        if self.model.check_vars[0].get() == 0 and \
                        self.model.check_vars[1].get() == 0 and \
                        self.model.check_vars[2].get() == 0:
            showwarning(title=WARNING_VERIFY_TITLE, message=WARNING_VERIFY_DESCR)
        else:
            from GUI.ClassificationFrame import ClassificationFrame
            ClassificationFrame(self.model, self.controller)
            self.destroy()

    def dataset_callback(self):
        """Callback for Crea Dataset button. Copy the new dataset in csv format to RScript/learning_file and in the
        learning files."""
        p = Processer(self.model)
        p.start()
        if self.model.dubious_counter == 0:
            if askyesno(ASK_DATASET_TITLE, ASK_DATASET_DESCR):
                if self.model.manual:
                    self.model.settings['knowledge_base_path'] = askdirectory(
                        title="Selezionare la directory della Knowledge Base:",
                        initialdir=self.model.settings['knowledge_base_path'])
                self.controller.add_dataset_to_learning()
        else:
            showwarning(title=WARNING_ERROR, message=WARNING_DOUBIOUS_PRESENT)
