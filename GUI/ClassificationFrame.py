# -*- coding: utf-8 -*-

import matplotlib
import platform

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from numpy import arange
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from Model.Constants import *
from GUI.Field import Field
from tkinter.messagebox import askokcancel, showwarning
from GUI.ResultFrame import ResultFrame
from os import getcwd



class ClassificationFrame(Toplevel):
    __doc__ = """GUI for the Manual Classification phase."""

    def __init__(self, model, controller, **options):
        # self.original_frame = original
        Toplevel.__init__(self, bg=BACKGROUND_COLOR, **options)
        self.title = TITLE_CLASSIFICATION
        self.protocol('WM_DELETE_WINDOW', self.quit)
        if platform.system() != 'Darwin':
            img = PhotoImage(file=getcwd() + '/res/img/breath.png')
            self.tk.call('wm', 'iconphoto', self._w, img)

        # model
        self.model = model
        # controller
        self.controller = controller

        # set the correct starter index, both for manual classification and verify classification.
        self.model.n = -1
        self.controller.get_next_curve_index()

        # Creating the main panel.
        self.create_parent_panel()

        # top-left
        self.create_top_left_frame()

        # top-right
        self.create_top_right_frame()

        # bottom
        self.create_bottom_frame()

        # bind keyboard event
        self.binder()

    def quit(self):
        """Override of the method quit. Ask before quitting all the program during the
        classification."""
        if askokcancel('Esci?', '       Vuoi veramente uscire?\n'
                                'Perderai il lavoro fatto fino ad ora.'):
            sys.exit()

    def create_parent_panel(self):
        """Create two parent panel. Panel1 is on the top. Panel2 is in the bottom of the main
        frame."""
        self.parent1 = Frame(self, height=FRAME_CLASSIFICATION_HEIGHT,
                             width=FRAME_CLASSIFICATION_WIDTH, bg=BACKGROUND_COLOR)
        self.parent1.pack(side=TOP, expand=False)
        self.parent2 = Frame(self, height=FRAME_CLASSIFICATION_HEIGHT,
                             width=FRAME_CLASSIFICATION_WIDTH, bg=BACKGROUND_COLOR)
        self.parent2.pack(side=BOTTOM, expand=False)

    def create_top_left_frame(self):
        """Create the top left panel containing the curve graphic."""
        self.draw_curve()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.parent1)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=LEFT)

    def create_top_right_frame(self):
        """Create the top right frame containing the variable entries. """
        self.f2 = Frame(self.parent1, bg=BACKGROUND_COLOR, height=FRAME_CLASSIFICATION_HEIGHT,
                        width=FRAME_CLASSIFICATION_WIDTH, padx=30,
                        pady=30)
        Label(self.f2, bg=BACKGROUND_COLOR, text=CLASSIFICATION_VALUES_TITLE, font=LABEL_TITLE_FONT).pack(
            side=TOP)
        self.f2.pack_propagate(0)
        self.f2.pack(side=RIGHT, expand=False)
        self.init_values_frame()

    def create_bottom_frame(self):
        """Create the bottom frame and all the navigation button."""
        self.f3 = Frame(self.parent2, bg=BACKGROUND_COLOR, height=int(FRAME_CLASSIFICATION_HEIGHT / 2),
                        width=2 * FRAME_CLASSIFICATION_WIDTH)
        self.f3.pack_propagate(0)
        self.f3.pack(side=BOTTOM, expand=True, padx=10, pady=(0, 10))

        self.f4 = Frame(self.f3, bg=BACKGROUND_COLOR, height=int(FRAME_CLASSIFICATION_HEIGHT / 4),
                        width=FRAME_CLASSIFICATION_WIDTH * 2)
        self.f4.pack_propagate(0)
        self.f4.pack(side=TOP, expand=True, padx=(0, 30), pady=(0, 10))
        self.f4_left = Frame(self.f4, bg=BACKGROUND_COLOR, height=int(FRAME_CLASSIFICATION_HEIGHT / 4),
                             width=(FRAME_CLASSIFICATION_WIDTH * 2) / 3)
        self.f4_left.pack_propagate(0)
        self.f4_left.pack(side=LEFT, expand=True, padx=(10, 10), pady=(0, 10))

        self.f4_right = Frame(self.f4, bg=BACKGROUND_COLOR, height=int(FRAME_CLASSIFICATION_HEIGHT / 4),
                              width=FRAME_CLASSIFICATION_WIDTH / 2)
        self.f4_right.pack_propagate(0)
        self.f4_right.pack(side=RIGHT, expand=True, padx=(10, 10), pady=(0, 10))

        # Ok button
        self.ok_button = Button(self.f4_left, width=7, text='OK', fg='black', bg=LIGHT_GREEN,
                                activebackground=ACTIVE_LIGHT_GREEN,
                                font=BUTTON_BIG_FONT, relief=RAISED, bd=2, command=self.ok_callback)
        self.ok_button.pack(side=LEFT)

        # Anomaly Button
        self.anom_button = Button(self.f4_left, width=7, text='Anomalia', fg='black', bg=LIGHT_RED,
                                  activebackground=ACTIVE_LIGHT_RED,
                                  font=BUTTON_BIG_FONT, relief=RAISED, bd=2,
                                  command=self.anomaly_callback)
        self.anom_button.pack(side=RIGHT)

        # Finish button
        self.finish_button = Button(self.f4_right, text=' Fine ', fg='black', bg=LIGHT_VIOLET,
                                    activebackground=ACTIVE_LIGHT_VIOLET,
                                    font=BUTTON_BIG_FONT, relief=RAISED, bd=2, padx=20,
                                    command=self.finish_callback)
        self.finish_button.pack(side=RIGHT)

        # Next Button
        self.next_button = Button(self.f3, text='Next', fg='black', bg=LIGHT_BLUE,
                                  activebackground=ACTIVE_LIGHT_BLUE,
                                  font=BUTTON_FONT, relief=RAISED, bd=2, command=self.next_callback)
        self.next_button.pack(side=RIGHT)

        # Previous button
        self.prev_button = Button(self.f3, text='Prev', fg='black', bg=LIGHT_BLUE,
                                  activebackground=ACTIVE_LIGHT_BLUE,
                                  font=BUTTON_FONT, relief=RAISED, bd=2, command=self.back_callback)
        self.prev_button.pack(side=LEFT)

        # Reset Button
        self.reset_button = Button(self.f3, text='Reset', fg='black', bg=LIGHT_BLUE,
                                   activebackground=ACTIVE_LIGHT_BLUE,
                                   font=BUTTON_FONT, relief=RAISED, bd=2,
                                   command=self.reset_callback)
        self.reset_button.pack()

    def draw_curve(self, color=None):
        """Draw the curve. Color param is used for specify the color of the curve."""
        if color is None:
            if self.model.curve_eadi[0, self.model.n] == ANOMALY:
                color = ANOMALY_COLOR_CURVE
            elif self.model.curve_eadi[0, self.model.n] == OK:
                color = OK_COLOR_CURVE
            else:
                color = DUBIOUS_COLOR_CURVE

        x = arange(1, PLOT_RANGE, 1)
        y = []
        for r in range(1, PLOT_RANGE):
            y.append(self.model.curve_eadi[r, self.model.n])

        self.figure = plt.figure(figsize=(5, 3), dpi=100, facecolor=BACKGROUND_COLOR)
        plt.axis([1, PLOT_RANGE, 0,
                  max(self.model.matricione[1, :]) + max(self.model.matricione[1, :]) / 10])
        self.subplot = self.figure.add_subplot(111)
        self.line2D, = self.subplot.plot(x, y, color)
        self.figure.canvas.draw()

    def init_values_frame(self):
        """Init the values in the top left frame."""
        self.field_tv = Field(self.f2, label='TV', entry=str(round(self.model.volume[self.model.n, 1], 4)),
                              pady=8)
        self.field_picco = Field(self.f2, label='Picco',
                                 entry=str(self.model.matricione[1, self.model.n]), pady=8)
        self.field_integrale = Field(self.f2, label='Integrale',
                                     entry=str(self.model.matricione[2, self.model.n]),
                                     pady=8)
        self.field_pi = Field(self.f2, label='P/I',
                              entry=str(self.model.matricione[3, self.model.n]), pady=8)
        self.field_curva = Field(self.f2, label='Curva',
                                 entry="{} di {}".format(str(self.model.n),
                                                         str(self.model.col - 1)), pady=8)

    def update_view(self):
        """Take all updated information from the Model and refresh the view."""
        self.update_fields()
        self.update_graph()

    def update_fields(self):
        """Update the content of all fields."""
        self.field_tv.set_variable(str(round(self.model.volume[self.model.n, 1], 4)))
        self.field_picco.set_variable(str(self.model.matricione[1, self.model.n]))
        self.field_integrale.set_variable(str(self.model.matricione[2, self.model.n]))
        self.field_pi.set_variable(str(self.model.matricione[3, self.model.n]))
        self.field_curva.set_variable("{} di {}".format(str(self.model.n), str(self.model.col - 1)))

    def update_graph(self, color=None):
        """Method that update the graph. Given a certain color, plot with it."""
        if color is None:
            if self.model.curve_eadi[0, self.model.n] == ANOMALY:
                color = ANOMALY_COLOR_CURVE
            elif self.model.curve_eadi[0, self.model.n] == OK:
                color = OK_COLOR_CURVE
            else:
                color = DUBIOUS_COLOR_CURVE

        plt.setp(self.line2D, color=color)

        new_y = []
        for r in range(1, PLOT_RANGE):
            new_y.append(self.model.curve_eadi[r, self.model.n])

        self.line2D.set_ydata(new_y)
        self.figure.canvas.draw()

    def next_callback(self):
        """Callback of next button."""
        self.controller.get_next_curve_index()
        self.update_view()

    def back_callback(self):
        """Callback of back button."""
        self.controller.get_prev_curve_index()
        self.update_view()

    def reset_callback(self):
        """Callback of reset button."""
        self.controller.get_first_curve_index()
        self.update_view()

    def anomaly_callback(self):
        """Callback of anomaly button."""
        if self.model.curve_eadi[0, self.model.n] != ANOMALY:
            if self.model.curve_eadi[0, self.model.n] == OK:
                self.model.ok_counter -= 1
            elif self.model.curve_eadi[0, self.model.n] == DUBIOUS:
                self.model.dubious_counter -= 1
            self.model.anomaly_counter += 1
            self.model.curve_eadi[0, self.model.n] = ANOMALY
            self.model.matricione[0, self.model.n] = ANOMALY
            self.update_graph(color=ANOMALY_COLOR_CURVE)

    def ok_callback(self):
        """Callback of OK button."""
        if self.model.curve_eadi[0, self.model.n] != OK:
            if self.model.curve_eadi[0, self.model.n] == ANOMALY:
                self.model.anomaly_counter -= 1
            elif self.model.curve_eadi[0, self.model.n] == DUBIOUS:
                self.model.dubious_counter -= 1
            self.model.curve_eadi[0, self.model.n] = OK
            self.model.matricione[0, self.model.n] = OK
            self.update_graph(color=OK_COLOR_CURVE)
            self.model.ok_counter += 1

    def finish_callback(self):
        """Callback of finish button."""
        if not self.model.manual:
            if self.model.check_vars[2].get() == 1 and self.model.dubious_counter != 0:
                showwarning("Attenzione", "Ci sono ancora delle curve dubbie.\nRicontrollale!")
            else:
                self.controller.save_csv()
                ResultFrame(self.model, self.controller)
                self.destroy()
        else:
            self.controller.save_csv()
            ResultFrame(self.model, self.controller)
            self.destroy()

    def binder(self):
        """Bind all button event. React to the arrow keys, to Enter key and BackSpace key."""
        self.bind('<Up>', (lambda event: self.next_callback()))
        self.bind('<Left>', (lambda event: self.back_callback()))
        self.bind('<Down>', (lambda event: self.back_callback()))
        self.bind('<Right>', (lambda event: self.next_callback()))
        self.bind('<Return'
                  '>', (lambda event: self.ok_anomaly_callback()))

    def ok_anomaly_callback(self):
        """Callback for the <Return> event generated by Enter key. If the curve is anomaly, turn it
        to ok and vice versa."""
        if self.model.curve_eadi[0, self.model.n] == ANOMALY or self.model.curve_eadi[0, self.model.n] == DUBIOUS:
            self.ok_callback()
        else:
            self.anomaly_callback()
