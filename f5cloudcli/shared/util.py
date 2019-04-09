""" Helper utility functions """
import os.path
import yaml

def multiply(n_1, n_2):
    """ Multiply two numbers """
    return n_1 * n_2

def getdoc():
    """ Get the docs """
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "../shared/help.yaml")
    with open(path, 'r') as file:
        docs = yaml.load(file)
        return docs
