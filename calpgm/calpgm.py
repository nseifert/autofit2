__author__ = 'Nathan Seifert'
import numpy as np
import os
import subprocess
import datetime


class Calpgm:
    # Common parameters for CALPGM.

    PARAMS_RIGID = {'A': 10000, 'B': 20000, 'C': 30000}
    PARAMS_QUART_A = {'-DelJ': 200, '-DelJK': 1100, '-DelK': 2000,
                      '-delJ': 40100, '-delK': 41000}
    PARAMS_QUART_S = {'-DJ': 200, '-DJK': 1100, '-DK': 2000,
                      'd1': 40100, 'd2': 50000}

    PARAMS_QUAD = {'1.5chi.aa': 110010000, '0.25chi(b-c)': 110040000,
                   'chi.ab': 110610000, 'chi.bc': 110210000,
                   'chi.ac': 110410000}

    ALL_PARAMS = dict(PARAMS_RIGID.items() + PARAMS_QUART_A.items()
                      + PARAMS_QUART_S.items() + PARAMS_QUAD.items())

    def add_params(self, new_params):

        """
        :param new_params: Dictionary of new CALPGM parameters
        to add to class. Key is name of variable and value is
        integer for CALPGM parameter
        :return: Returns True if successful. Throws error if new_params is empty.
        """

        if not new_params:
            return 0  # EXCEPT NEEDED
        for key, value in new_params.iteritems():
            if not isinstance(key, basestring):
                return 0  # EXCEPT NEEDED
            try:
                new_params[key] = int(value)  # in case it's a string
            except ValueError:
                return 0  # EXCEPT NEEDED; Not an integer

        else:
            self.ALL_PARAMS = dict(self.ALL_PARAMS.items()
                                   + new_params.items())

            return True

    @staticmethod
    def calc_spin(input_spin):

        """
        :param input_spin: Integer corresponding to nuclear spin
        (e.g. for no hyperfine, input_spin should be 0).
        :return: Integer corresponding to spin input needed for
        CALPGM input (nuclear spin 0 --> CALPGM 1; Nitrogen (spin 1)
        ---> CALPGM 3)
        """

        if input_spin == np.floor(float(input_spin)):
            input_spin = int(2 * float(input_spin) + 1)
        else:
            input_spin = 2 * int(np.ceil(float(input_spin)))

        return input_spin

    def from_file(self, input_str):
        # Processes data from file as string
        # input_str can be file path or text stream?
        # Returns a dictionary that will be read into read_data
        pass

    def read_data(self, input_data):
        # Processes input data from dictionary
        # Need to handle instance where new parameter might not be in list?
        # Input can either be by parameter # or name????
        pass

    def __init__(self, **kwargs):
        """

        :param kwargs: Dictionary containing essential
        initialization parameters for SPCAT/SPFIT instances.
        :return: No return.
        """

        self.defaults = {'name': 'molecule', 'filename': 'default',
                         'max_freq': 20.0, 'dipoles': [1.0, 1.0, 1.0],
                         'temp': 2.0, 'spin': 0.0, 'reduction': 'a',
                         'J_min': 0, 'J_max': 20, 'inten_cutoff': -10.0}

        print 'CALPGM constructor initialized\n'

        self.params = self.defaults.copy()
        self.params.update(kwargs)

        if 'new_params' in self.params:
            self.add_params(self.params['new_params'])

        if 'data' in self.params:

            # MIGHT NEED TO BE CHANGED. Not 100% sure how data needs to be formatted

            if isinstance(self.params['data'], basestring):
                self.read_data(self.from_file(self.params['data']))
            else:
                self.read_data(self.params['data'])
