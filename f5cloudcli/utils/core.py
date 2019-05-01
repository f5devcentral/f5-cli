""" Core utility functions """

import os

def multiply(n_1, n_2):
    """ Multiply two numbers """
    return n_1 * n_2

def convert_to_absolute(file):
    """Convert file to absolute path """
    return os.path.abspath(os.path.join(os.getcwd(), file))
