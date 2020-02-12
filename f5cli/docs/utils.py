"""Denotes directory is a package """

import os
import yaml


def get_docs():
    """ Get the docs """
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, 'help.yaml')
    with open(path, 'r') as file:
        docs = yaml.safe_load(file)
    return docs
