# -*- coding: utf-8 -*-
import csv
from threading import Thread

import numpy as np

from Model.Constants import *


class Processer:
    __doc__ = """Class responsable of the creation of the final dataset."""

    def __init__(self, model):
        self.model = model
        t = Thread(target=self.start(), name='t-processer')
        t.start()

    def start(self):
        self.retrieve_features()
        self.create_csv()

    def retrieve_features(self):
        # RR / TV
        self._retreive_rr_over_tv()

        # ETCO2 - End Tidal CO2: scale: 0.100000 unit: %
        self._retreive_etco2()

        # Last curve value not equal to 0
        self._retreive_last_value()

        # Intercetta: mean of first 15 values.
        self._intercetta()

        # integral after max
        self._integral_after_max()

        self._evaluate_concavity()

    def _retreive_rr_over_tv(self):
        """Retrive the RR over TV attribute. Set -inf, inf, NaN to 0."""
        with np.errstate(divide='ignore', invalid='ignore'):
            self.rr_over_tv = np.true_divide(self.model.matricione[5, :], self.model.matricione[6, :])
            self.rr_over_tv[~ np.isfinite(self.rr_over_tv)] = 0  # -inf, inf, NaN

    def _retreive_etco2(self):
        """Safe retreive of etco2 informations."""
        if self.model.c is None:
            for file_path in self.model.trend_rr_insp_paths:
                with open(file_path) as f:
                    if self.model.c is None:
                        self.model.c = np.loadtxt(f, comments="%", usecols=(3, 4, 6))
                    else:
                        self.model.c = np.concatenate((self.model.c,
                                                       np.loadtxt(f, comments="%", usecols=(3, 4, 6))))

        self.etco2 = self.model.c[:, 2]
        for i in range(1, self.etco2.shape[0] - 1):
            if self.etco2[i] == 9999 or self.etco2[i] == 0:
                self.etco2[i] = (self.etco2[i - 1] + self.etco2[i + 1]) / 2

    def _retreive_last_value(self):
        """retreive the last value of the curve not equal to zero."""
        (max_row_num, max_col_num) = self.model.curve_eadi.shape
        self.last_value = np.zeros(max_col_num)

        for col_idx in range(max_col_num):
            row_idx = max_row_num - 1
            while row_idx > 2:
                if float(self.model.curve_eadi[row_idx, col_idx]) == 0.0:
                    row_idx -= 1
                else:
                    self.last_value[col_idx] = self.model.curve_eadi[row_idx, col_idx]
                    break

    def _intercetta(self):
        """Get the mean value of the first 15 elements of the curve."""
        self.intercetta = np.zeros(self.model.curve_eadi.shape[1])
        for col in range(self.model.curve_eadi.shape[1]):
            self.intercetta[col] = np.mean(self.model.curve_eadi[:, col])

    def _integral_after_max(self):
        """Get the integral of the area after the max value (picco)."""
        (max_row_num, max_col_num) = self.model.curve_eadi.shape
        # self.integral_after_max = np.array([])
        self.integral_after_max = np.zeros(max_col_num)
        # self.max_idx = np.array([])
        self.max_idx = np.zeros(max_col_num)

        for col in range(max_col_num):
            self.max_idx[col] = np.argmax(self.model.curve_eadi[:, col])
            self.integral_after_max[col] = np.sum(self.model.curve_eadi[int(self.max_idx[col]):, col])

    def _evaluate_concavity(self):
        """Evaluate all the concavity of the curve."""
        # Initialization of attributes:
        self.before_concavity_counters = np.array([], dtype=np.int64)
        self.after_concavity_counters = np.array([], dtype=np.int64)
        self.before_areas = np.zeros((self.model.col, NUM_MAX_CONCAVITY), dtype=np.float64)
        self.after_areas = np.zeros((self.model.col, NUM_MAX_CONCAVITY), dtype=np.float64)

        # First derivate
        self._get_first_derivate()
        # Evaluate first derivate
        self._find_max_min_()

        # Sort
        self.before_areas.sort()
        self.after_areas.sort()

    def _get_first_derivate(self):
        """Compute the first derivate of all curve."""
        _curve_eadi_t = self.model.curve_eadi.T
        _curve_eadi_t = _curve_eadi_t[:, 1:]
        (max_row_num, max_col_num) = _curve_eadi_t.shape
        self.first_derivate = np.full((max_row_num, max_col_num - 2), -1, dtype=np.float64)
        # compute the approx first derivate.
        for row in range(max_row_num):
            # start from 1 in order to compute the approx derivate
            for col in range(1, max_col_num - 2):
                if col > 2 and _curve_eadi_t[row, col + 1] == 0:
                    break
                else:
                    self.first_derivate[row, col - 1] = (_curve_eadi_t[row, col + 1] -
                                                         _curve_eadi_t[row, col - 1]) / 2

    def _find_max_min_(self):
        """Count the number of concativities."""
        self.max_min_list = []
        (curve_idx_max, fd_point_idx_max) = self.first_derivate.shape
        row = 0
        count = 0

        for first_deriv in self.first_derivate:
            for fd_i in range(fd_point_idx_max - 1):
                if first_deriv[fd_i] > 0 and first_deriv[fd_i + 1] < 0:
                    # fd_i is a point of LOCAL MAXIMUM
                    self.max_min_list.append((fd_i + 1, 'MAX'))
                    count += 1
                elif first_deriv[fd_i] < 0 and first_deriv[fd_i + 1] > 0:
                    # fd_i is a point of LOCAL MINIMUM
                    self.max_min_list.append((fd_i + 1, 'MIN'))
                    count += 1
                elif first_deriv[fd_i] == 0 and fd_i > 0:
                    if first_deriv[fd_i - 1] > 0:
                        # fd_i is a point of LOCAL MAXIMUM
                        self.max_min_list.append((fd_i + 1, 'MAX'))
                        count += 1
                    elif first_deriv[fd_i - 1] == 0:
                        pass
                    else:  # if first_deriv[fd_i - 1] < 0
                        # fd_i is a point of LOCAL MINIMUM
                        self.max_min_list.append((fd_i + 1, 'MIN'))
                        count += 1

            self._evaluate_max_min(row)
            self.max_min_list = []
            row += 1

    def _evaluate_max_min(self, row):
        """Evaluates what kind of concavity it is."""
        bef_conc_counter = 0
        aft_conc_counter = 0

        for index in range(len(self.max_min_list)):
            key, value = self.max_min_list[index]
            try:
                next_key, next_value = self.max_min_list[index + 1]

                if value == 'MAX' and next_value == 'MIN':
                    if int(key) != int(self.max_idx[row]):
                        # Compute the area.
                        area = self._calculate_max_min_integral(row, int(key), int(next_key))
                        # include it in the correct list.
                        if int(key) < int(self.max_idx[row]):
                            self.before_areas[row, bef_conc_counter] = area
                            bef_conc_counter += 1
                        else:
                            self.after_areas[row, aft_conc_counter] = area
                            aft_conc_counter += 1
                        index += 2
            except IndexError:
                break

        # update general counters
        self.before_concavity_counters = np.append(self.before_concavity_counters, bef_conc_counter)
        self.after_concavity_counters = np.append(self.after_concavity_counters, aft_conc_counter)

    def _calculate_max_min_integral(self, curve_index, idx_max, idx_min):
        """Calculate the integral of the area under the curve until the minimum value of the
        curve."""
        area = 0
        for i in range(idx_max, idx_min):
            area += abs(
                self.model.curve_eadi[i, curve_index] - self.model.curve_eadi[idx_min, curve_index])
        return area * 2

    def create_csv(self):
        """Create the final CSV dataset file."""
        with open(self.model.settings['working_directory_path'] + "dataset.csv", 'w') as csv_fd:
            fieldnames = ['classification', 'picco', 'integral', 'pi_index', 'tidal_volume', 'resp_rate',
                          'rr_over_tv', 'etco2', 'first_value', 'last_value', 'intercetta',
                          'integral_after_max', 'before_concavity_counter', 'before_area_1',
                          'before_area_2', 'before_area_3', 'after_concavity_counter', 'after_area_1',
                          'after_area_2', 'after_area_3']
            writer = csv.DictWriter(csv_fd, fieldnames=fieldnames)
            writer.writeheader()

            for row in range(self.model.col):
                writer.writerow(
                    {'classification': self.model.matricione[0, row], 'picco': self.model.matricione[1, row],
                     'integral': self.model.matricione[2, row], 'pi_index': self.model.matricione[3, row],
                     'tidal_volume': self.model.matricione[6, row], 'resp_rate': self.model.matricione[5, row],
                     'rr_over_tv': self.rr_over_tv[row], 'etco2': self.etco2[row],
                     'first_value': self.model.curve_eadi[2, row], 'last_value': self.last_value[row],
                     'intercetta': self.intercetta[row],
                     'integral_after_max': self.integral_after_max[row],
                     'before_concavity_counter': self.before_concavity_counters[row],
                     'before_area_1': self.before_areas[row, 0],
                     'before_area_2': self.before_areas[row, 1],
                     'before_area_3': self.before_areas[row, 2],
                     'after_concavity_counter': self.after_concavity_counters[row],
                     'after_area_1': self.after_areas[row, 0], 'after_area_2': self.after_areas[row, 1],
                     'after_area_3': self.after_areas[row, 2]})
