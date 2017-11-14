# -*- coding: utf-8 -*-

class Model:
    __doc__ = '''The Model class stores all the informations shared between all elements of the GUI and the
    controller.'''

    def __init__(self):
        # Specify if the model is used for manual (True) or automatic (False).
        self.manual = True

        # pointer to the original frame.
        self.original_frame = None

        # working directory path
        # self.working_directory = None
        # learning directory path
        # self.learning_directory = None

        # inside there are sensibility, working_directory and learning_directory.
        self.settings = None

        # servo curve path
        self.servo_curve_paths = []
        # trend tidal path
        self.trend_tidal_volume_paths = []
        # trend rr insp path
        self.trend_rr_insp_paths = []

        self.csv_output_path = None

        self.edi = None
        # inspired volume.
        self.volume = None
        self.c = None
        # data point of the curve
        self.curve_eadi = None
        # final big matrix containing all the information
        self.matricione = None
        # number of column
        self.col = None
        # progressive curve number.
        self.n = 0

        # counters
        self.ok_counter = 0
        self.anomaly_counter = 0
        self.dubious_counter = 0

        # sensibility
        # self.sensibility = DEFAULT_ALPHA_TRESHOLD

        # state of Check Buttons = [an_var, ok_var, doub_var]
        self.check_vars = []
