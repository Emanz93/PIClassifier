# -*- coding: utf-8 -*-
import json
from csv import reader, writer
from os import listdir, getcwd, unlink
from os.path import isfile, isdir, join
from shutil import copy, copy2
from subprocess import check_output
from threading import Thread
from tkinter.messagebox import askyesno, showerror
from operator import xor

import numpy as np

from Controller.Processer import Processer
from GUI.ClassificationFrame import ClassificationFrame
from GUI.ResultFrame import ResultFrame
from Model.Constants import *


class Controller:
    __doc__ = """Controller Class for the Manual Classification phase. It is robust between multiple split files."""

    def __init__(self, model):
        """Costructor of the Controller. Init the model. Waiting the classification type."""
        self.model = model
        # update the model knowledge base path.
        self.restore_json_settings()
        # t_consistency = Thread(target=self.check_consistency, name='t-consistency')
        # t_consistency.start()

    def start(self):
        """Start the classification based on the method chosen."""
        # Choose the loading method.
        if self.model.manual is True:  # Manual Classification
            self.class_frame = ClassificationFrame(self.model, self)
        else:  # Automatic Classification
            """Raise a error when in automatic classification we are trying to classify some work already
                    done."""
            self.automatic_classification()
            self.auto_frame = ResultFrame(self.model, self)

    def choose_work(self):
        """Choose the loading method for retrieve all information."""
        if self.model.manual:
            if MATRICIONE_CSV_NAME in listdir(self.model.settings['working_directory_path']) \
                    and CURVE_EADI_CSV_NAME in listdir(self.model.settings['working_directory_path']):
                if askyesno(title=POPUP_C_TITLE, message=POPUP_C_MESSAGE):
                    self.load_previous_work()
                else:
                    self.load_new_work()
            else:
                self.load_new_work()
        else: # self.model.manual = False -> AUTOMATIC CLASSIFICATION
            if MATRICIONE_CSV_NAME in listdir(self.model.settings['working_directory_path']) \
                    and CURVE_EADI_CSV_NAME in listdir(self.model.settings['working_directory_path']):
                if not askyesno(title=POPUP_C_TITLE, message=POPUP_C_MESSAGE_AUTOM):
                    return False
                self.load_new_work()

    def load_previous_work(self):
        """Restart a previous work."""
        t1 = Thread(target=self.load_matricione, name='t-loadmatr')
        t1.start()
        t2 = Thread(target=self.load_servo_curve, name='t-loadservocurve')
        t2.start()
        t3 = Thread(target=self.load_volume(), name='t-volume')
        t3.start()
        t1.join()
        t2.join()
        t3.join()

    def load_new_work(self):
        """Start a new work. Load Servo Data, Volume Data and RR Data."""
        t1 = Thread(target=self.load_servo(), name='t-servo')
        t1.start()
        t2 = Thread(target=self.load_volume(), name='t-volume')
        t2.start()
        t3 = Thread(target=self.load_rr(), name='t-rr')
        t3.start()
        t1.join()
        t2.join()
        t3.join()

        self.retrieve_all_information()

    def load_servo(self):
        """Load the data of the Servo Curve File(s). Append the content of the files in a unique
        ndarray, called edi, stored in the model."""
        for file_path in self.model.servo_curve_paths:
            with open(file_path) as f:
                if self.model.edi is None:
                    self.model.edi = np.loadtxt(file_path, comments="%", usecols=(3, 4, 5, 6))
                else:
                    self.model.edi = np.concatenate((self.model.edi, np.loadtxt(file_path, comments="%", usecols=(3, 4, 5, 6))))

    def load_volume(self):
        """Load the data from the Trend Tidal Volume File(s) and append the content of the files in
        a unique ndarray, called volume, stored in model."""
        for file_path in self.model.trend_tidal_volume_paths:
            with open(file_path) as f:
                if self.model.volume is None:
                    self.model.volume = np.round((np.loadtxt(file_path, comments="%", usecols=(3, 4)) / 10000000), 3)
                else:
                    self.model.volume = np.concatenate((self.model.volume, np.round(
                        (np.loadtxt(file_path, comments="%", usecols=(3, 4)) / 10000000), 3)))

        v = np.shape(self.model.volume)
        self.model.col = v[0]
        self.model.ok_counter = v[0]

    def load_rr(self):
        """Load the rr data from the Trend RR Files. Append the content of the files in a unique
        ndarray, called c. It is stored in the model."""
        for file_path in self.model.trend_rr_insp_paths:
            with open(file_path) as f:
                if self.model.c is None:
                    self.model.c = np.loadtxt(file_path, comments="%", usecols=(3, 4, 6))
                else:
                    self.model.c = np.concatenate((self.model.c, np.loadtxt(file_path, comments="%", usecols=(3, 4, 6))))

    def retrieve_all_information(self):
        """Retrieve all information from the input files."""
        # rows = number of ponts of edi curve
        rows = np.shape(self.model.edi)[0]
        total_number_data = 400
        eadi_provvisorio = np.zeros([total_number_data, self.model.col])
        insp = np.zeros([total_number_data, self.model.col])
        RR = self.model.c[:, 1]
        colonna = 0
        riga = 0
        incr = 1

        for punt in range(0, rows - 1):
            if (self.model.edi[punt, 0] == 1) and (incr > 0):
                try:
                    # In eadi_provvisorio insert only eadi of inspiration phase (breath_pase == 1) .
                    eadi_provvisorio[riga, colonna] = self.model.edi[punt, 3]
                    insp[riga, colonna] = self.model.edi[punt, 0]
                    riga += 1
                    incr += 1
                    continue
                except IndexError:
                    break
            if incr > 1:
                colonna += 1
                incr = 1
                riga = 1

        # Normalization of eadi.
        self.model.eadi = np.round(eadi_provvisorio / 100, 2)

        # compute the picco as max of all eadi points.
        picco = np.max(self.model.eadi, axis=0)

        # compute the integral as the sum of all point of eadi curve
        integral = np.sum(self.model.eadi, axis=0)
        integral = np.round(integral, 0)

        # t_insp is the sum of all
        t_insp = np.sum(insp, axis=0)

        # picco/integral
        # fixed divide by zero problem!!! 0/0 = 0 and 123/0 = 0. This is made for
        # pi = np.divide(picco, integral)
        with np.errstate(divide='ignore', invalid='ignore'):
            pi = np.divide(picco, integral)
            pi[~ np.isfinite(pi)] = 0

        pi = np.round(pi * 1000, 1)

        self.model.curve_eadi = np.insert(self.model.eadi, 0, 1, axis=0)
        # in the matricione the last element is the type. Fixed by automatic controller.
        # 1 : Ok
        # 0 : Anomaly
        # 2 : Dubious
        if picco is None:
            print("retrieve_all_information: picco is None.")
        if integral is None:
            print("retrieve_all_information: integral is None.")
        if pi is None:
            print("retrieve_all_information: pi is None.")
        if t_insp is None:
            print("retrieve_all_information: t_insp is None.")
        if RR is None:
            print("retrieve_all_information: RR is None.")
        if self.model.volume is None:
            print("retrieve_all_information: self.model.volume is None.")


        matricione_provvisorio = np.column_stack((picco, integral, pi, t_insp, RR,
                                                  self.model.volume[:, 1],
                                                  np.ones(np.shape(picco), dtype=np.float64)))
        self.model.matricione = np.insert(matricione_provvisorio.T, 0, 1, axis=0)
        if self.model.matricione is None:
            print("retrieve_all_information: matricione is None.")

        self.model.n = 0

    def save_csv(self):
        """Wrapper which saves all the output file. They will be stored in the working directory."""
        t1 = Thread(target=self.save_matricione(), name='t-saveMatrCSV')
        t1.start()
        t2 = Thread(target=self.save_servo_curve(), name='t-saveCurveCSV')
        t2.start()
        t1.join()
        t2.join()

    def save_matricione(self):
        """Save all important information in a csv file called Matricione."""
        with open(self.model.settings['working_directory_path'] + MATRICIONE_CSV_NAME, 'w') as csv_fd:
            csv_writer = writer(csv_fd)
            for values in self.model.matricione:
                csv_writer.writerow(values)

    def load_matricione(self):
        """Load a previous Matricione.csv from the Working Directory."""
        with open(self.model.settings['working_directory_path'] + MATRICIONE_CSV_NAME, 'r') as csv_fd:
            csv_reader = reader(csv_fd, delimiter=",")
            self.model.matricione = np.array(list(csv_reader)).astype("float")

        # load old work
        for classification in self.model.matricione[0]:
            if classification == ANOMALY:
                self.model.anomaly_counter += 1
            if classification == OK:
                self.model.ok_counter += 1
            if classification == DUBIOUS:
                self.model.dubious_counter += 1

    def load_servo_curve(self):
        """Load a previous Curve_Eadi.csv from the Working Directory."""
        with open(self.model.settings['working_directory_path'] + CURVE_EADI_CSV_NAME, 'r') as csv_fd:
            csv_reader = reader(csv_fd, delimiter=",")
            self.model.curve_eadi = np.array(list(csv_reader)).astype("float")

    def save_servo_curve(self):
        """Save the Servo Curve data used to plot the graph in the Classification Phase."""
        with open(self.model.settings['working_directory_path'] + CURVE_EADI_CSV_NAME, 'w') as csv_fd:
            csv_writer = writer(csv_fd)
            for values in self.model.curve_eadi:
                csv_writer.writerow(values)

    def init_learning_directory(self):
        """Safe copy of the learning dataset into the ./RScript/learning_files folder. Check also the consistency
        of the .csv files."""
        # Here I need to remove all the files in the ./RScript/learning_files
        if self.model.settings['knowledge_base_path'] != getcwd() + LEARNING_FILES_PATH[1:]:
            for file in listdir(LEARNING_FILES_PATH):
                file_path = join(LEARNING_FILES_PATH, file)
                try:
                    if isfile(file_path):
                        unlink(file_path)
                except Exception as e:
                    print('Failed to remove {}'.format(file_path))
                    print(e)

            # After that, I need to copy *.csv files into the ./RScript/learning_files
            for file in listdir(self.model.settings['knowledge_base_path']):
                file_path = join(self.model.settings['knowledge_base_path'] + file)
                if file_path.endswith('.csv') and self.check_consistency(file_path):
                    try:
                        copy2(file_path, LEARNING_FILES_PATH)
                    except IOError as e:
                        print(e)

    def automatic_classification(self):
        """Do the Automatic Classification."""
        # save the csv.
        self.automatic_processer = Processer(self.model)
        self.automatic_processer.start()

        self.init_learning_directory()

        # launch_automatic_classification by R script.
        self.call_r_script()
        # do the real classification in three parts:
        self.automatic_decision()
        # save matricione and curve eadi CSVs.
        self.save_csv()

    def call_r_script(self):
        """Call the R script with the classification method. Return an array of probability."""
        command = R_SCRIPT
        path2script = R_SCRIPT_PATH
        arg = self.model.settings['working_directory_path'] + DATASET_NAME

        cmd = [command, path2script, arg]

        res_string = check_output(cmd, universal_newlines=True)
        res_list = res_string.split(" ")
        self.model.res_prob = np.zeros(len(res_list), dtype=np.float64)
        for i in range(len(res_list)):
            self.model.res_prob[i] = float(res_list[i])

    def automatic_decision(self):
        """Do the classification of the array of probability using the threshold. Update the counters
        and update the matricione and curve_eadi."""
        ok_treshold = 1 - self.model.settings['sensibility']
        an_treshold = self.model.settings['sensibility']
        i = 0
        self.model.ok_counter = 0
        self.model.anomaly_counter = 0
        self.model.dubious_counter = 0

        for prob in self.model.res_prob:
            if prob > ok_treshold:
                self.model.matricione[0, i] = OK
                self.model.curve_eadi[0, i] = OK
                self.model.ok_counter += 1
            elif prob < an_treshold:
                self.model.matricione[0, i] = ANOMALY
                self.model.curve_eadi[0, i] = ANOMALY
                self.model.anomaly_counter += 1
            else:
                self.model.matricione[0, i] = DUBIOUS
                self.model.curve_eadi[0, i] = DUBIOUS
                self.model.dubious_counter += 1
            i += 1

    def get_next_curve_index(self):
        """Increment self.model.n to the next curve."""
        if self.model.manual is True:  # Manual Case
            self.model.n += 1
            if self.model.n > self.model.col - 1:
                self.model.n = 0
        else:  # Automatic Case
            old_n = self.model.n
            self.model.n += 1
            while self.model.n != old_n:
                if self.model.n > self.model.col - 1:
                    self.model.n = 0
                # go ahead only for the set of curves selected.
                if self.model.check_vars[0].get() == 1 and self.model.matricione[0, self.model.n] == ANOMALY:
                    break
                elif self.model.check_vars[1].get() == 1 and self.model.matricione[0, self.model.n] == OK:
                    break
                elif self.model.check_vars[2].get() == 1 and self.model.matricione[0, self.model.n] == DUBIOUS:
                    break
                self.model.n += 1

    def get_prev_curve_index(self):
        """Decrement self.model.n to the previous curve."""
        if self.model.manual is True:  # Manual Case
            self.model.n -= 1
            if self.model.n < 0:
                self.model.n = self.model.col - 1
        else:  # Automatic Case
            old_n = self.model.n
            self.model.n -= 1
            while self.model.n != old_n:
                if self.model.n < 0:
                    self.model.n = self.model.col - 1
                if self.model.check_vars[0].get() == 1 and self.model.matricione[0, self.model.n] == ANOMALY:
                    break
                elif self.model.check_vars[1].get() == 1 and self.model.matricione[0, self.model.n] == OK:
                    break
                elif self.model.check_vars[2].get() == 1 and self.model.matricione[0, self.model.n] == DUBIOUS:
                    break
                self.model.n -= 1

    def get_first_curve_index(self):
        """Set self.model.n to the first index. Used by reset button in the classification view."""
        if self.model.manual is True:  # Manual Case
            self.model.n = 0
        else:  # Automatic Case
            self.model.n = 0
            while self.model.n != self.model.col:
                if self.model.check_vars[0].get() == 1 and self.model.matricione[0, self.model.n] == ANOMALY:
                    break
                elif self.model.check_vars[1].get() == 1 and self.model.matricione[0, self.model.n] == OK:
                    break
                elif self.model.check_vars[2].get() == 1 and self.model.matricione[0, self.model.n] == DUBIOUS:
                    break
                self.model.n += 1

    def add_dataset_to_learning(self):
        """Add the current dataset to the learning datasets."""
        dataset_path = self.model.settings['working_directory_path'] + DATASET_NAME
        split = self.model.settings['working_directory_path'].split("/")
        new_name = split[-2] + '.csv'

        copy(dataset_path, LEARNING_FILES_PATH + new_name)
        copy(dataset_path, self.model.settings['knowledge_base_path'] + '/' + new_name)

    def restore_json_settings(self):
        """Restore all the information from the json settings file. Safe restore. Check if the json is empty!"""
        # read the json file.
        with open(getcwd() + '/Model/settings.json', 'r') as f:
            self.model.settings = json.load(f)

        if self.model.settings['knowledge_base_path'] == '':
            self.model.settings['knowledge_base_path'] = getcwd()

        if self.model.settings['working_directory_path'] == '':
            self.model.settings['working_directory_path'] = getcwd()

    def save_json_settings(self):
        """Save the json settings after the work."""
        self.model.settings['knowledge_base_path'] = self.model.settings['knowledge_base_path']
        self.model.settings['working_directory_path'] = self.model.settings['working_directory_path']

        with open(getcwd() + '/Model/settings.json', 'w') as f:
            json.dump(self.model.settings, f)

    def check_consistency(self, file_path):
        """Check the consistency of the learning dataset """
        try:
            with open(file_path, 'r') as f:
                r = reader(f)
                dataset = np.array(list(r))
                h = np.array(
                    ['classification', 'picco', 'integral', 'pi_index', 'tidal_volume', 'resp_rate', 'rr_over_tv',
                     'etco2',
                     'first_value', 'last_value', 'intercetta', 'integral_after_max', 'before_concavity_counter',
                     'before_area_1', 'before_area_2', 'before_area_3', 'after_concavity_counter', 'after_area_1',
                     'after_area_2', 'after_area_3'], dtype='<U24')
                return np.array_equal(h, dataset[0, :])
        except FileNotFoundError as e:
            print('file_path={}'.format(file_path))
            print(e)

    def _retrieve_input_files_paths(self):
        """ Get the list of all files paths. Look for:
        - *TrendRRInspTime*.nta
        - *ServoCurveData*.nta
        - *TrendTidalVolume*.nta
        - Curves_*.sta
        - Breath_*.sta
        """
        for file in listdir(self.model.settings['working_directory_path']):
            if not file.startswith('.'):
                if RR_REGEX in file and file.endswith(OLD_INPUT_FILE_EXTENSION):
                    self.model.trend_rr_insp_paths.append(self.model.settings['working_directory_path'] + file)
                elif SERVO_REGEX in file and file.endswith(OLD_INPUT_FILE_EXTENSION):
                    self.model.servo_curve_paths.append(self.model.settings['working_directory_path'] + file)
                elif VOLUME_REGEX in file and file.endswith(OLD_INPUT_FILE_EXTENSION):
                    self.model.trend_tidal_volume_paths.append(self.model.settings['working_directory_path'] + file)
                elif CURVES_REGEX in file and file.endswith(NEW_INPUT_FILE_EXTENSION):
                    self.model.curves_paths.append(self.model.settings['working_directory_path'] + file)
                elif BREATH_REGEX in file and file.endswith(NEW_INPUT_FILE_EXTENSION):
                    self.model.breath_paths.append(self.model.settings['working_directory_path'] + file)

    def check_valid_wd(self):
        """Retrieve all the path for the servo, volume and rr files, given the working directory
        path."""
        if isdir(self.model.settings['working_directory_path']):

            self._retrieve_input_files_paths()

            if len(self.model.trend_rr_insp_paths) == 0 or \
                            len(self.model.servo_curve_paths) == 0 or \
                            len(self.model.trend_tidal_volume_paths) == 0:
                self.model.trend_rr_insp_paths = []
                self.model.servo_curve_paths = []
                self.model.trend_tidal_volume_paths = []
                showerror(title="Attenzione",
                          message="Directory di lavoro non valida. Questa deve contenere:\n"
                                  "  - TrendRRInspTime... .nta\n"
                                  "  - ServoCurveData... .nta\n"
                                  "  - TrendTidalVolume... .nta\n\n"
                                  "Prego, selezionare un altra cartella.")
                return False
            else:
                return True
        else:
            showerror(title="Attenzione",
                      message="Directory di lavoro non valida. Selezionarne un altra.")
            return False

    def check_valid_ld(self):
        """Check if the Knowledge Base is valid. ATTENTION: DUMMY CHECK. Future work is to be a correct validation
        of the csv learning files content."""
        if self.model.manual:
            return True
        if isdir(self.model.settings['knowledge_base_path']):
            for file in listdir(self.model.settings['knowledge_base_path']):
                file_path = self.model.settings['knowledge_base_path'] + file
                if not file.startswith('.') and file.endswith('.csv') and self.check_consistency(file_path):
                    return True
        showerror(title="Attenzione",
                  message="Directory della Knowledge Base non valida. Deve esserci almeno un file di learning (.csv) generato dal programma."
                          "E' possibile generarli grazie alla Classificazione Manuale.")
        return False
