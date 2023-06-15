# -*- encoding: utf-8 -*-
# src/utils/evaluations.py
# Evaluation functions for experiments.


import random

def sample_error(bound):
    """Sample an error givena its bound"""

    return random.randint(- bound, + bound)
