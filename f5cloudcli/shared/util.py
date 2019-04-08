""" Helper utility functions """
import yaml

def multiply(n_1, n_2):
    """ Multiply two numbers """
    return n_1 * n_2

def getdoc():
    """ Get the docs """
    with open('f5cloudcli/shared/help.yaml', 'r') as file:
        docs = yaml.load(file)
        return docs
