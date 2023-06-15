# -*- encoding: utf-8 -*-
# src/lib/message.py
# Class for message vector (matrices) operations.

import random

from src.utils.evaluations import sample_error
from src.utils.os import log_error, exit_with_error


class Message:

    def __init__(self, mod=None, rows=None, cols=None, message=None):
        """Initialize a message vector"""

        self.mod = mod
        self.rows = rows
        self.cols = cols
        self.message = message


    ############################
    #      Private methods 
    ############################

    def _check_dimensions(self, other_msg) -> None:
        """Check the dimensions of two matrices"""

        if self.rows != other_msg.rows or self.cols != other_msg.cols:
                log_error(f'Matrices have different dimensions:')
                exit_with_error(f'{self.rows}x{self.cols} and {other_msg.rows}x{other_msg.cols}')

    def __add__(self, vector):
        """Add two matrices"""

        self._check_dimensions(vector)
        
        for i in range(len(self.message)):
            self.message[i] = (self.message[i] + vector.message[i]) % self.mod

        return self

    def __sub__(self, vector):
        """Subtract two matrices"""

        self._check_dimensions(vector)

        for index in range(len(self.message)):
            self.message[index] = (self.message[index] - vector.message[index]) % self.mod
        
        return self

    def __mul__(self, vector):
        """Multiply two matrices"""

        this_vector = [0] * (self.rows * vector.cols)

        # TODO: Optimize this
        for i in range(self.rows):
            for j in range(self.cols):
                for k in range(vector.cols):
                    this_vector[i * vector.cols + k] = (this_vector[i * vector.cols + k] + \
                                                       (self.message[i * self.cols + j] * \
                                                       vector.message[j * vector.cols + k])) % self.mod
        
        return Message(self.mod, self.rows, vector.cols, this_vector)
    
    def __eq__(self, vector):
        """Check if two matrices are equal"""

        return (self.rows == vector.rows) and \
               (self.cols == vector.cols) and \
               (self.message == vector.message)

    def __repr__(self):
        """Print the message vector"""

        return f'\nRows: {self.rows}\nCols: {self.cols}\nVector: {self.message}\n'


    ############################
    #     Public methods 
    ############################

    def calculate_scaling(self, numerator, denominator, this_mod):
        """Calculate the scaled message vector"""

        this_vector = [0] * (self.rows * self.cols)

        for i in range(len(self.message)):
            this_vector[i] = round((numerator * self.message[i]) / denominator) % this_mod

        return Message(this_mod, self.rows, self.cols, this_vector)

    def set_query_element(self, row, col, value) -> None:
        """Set the value at a particular index"""

        self.message[row * self.cols + col] = value
        
    def get_query_element(self, row, col) -> int:
        """Get the value at a particular index"""

        return self.message[row * self.cols + col]


    ############################
    #     Static methods 
    ############################

    @staticmethod
    def create_random_message(mod, rows, cols): 
        """Create a random message vector"""

        return Message(mod, rows, cols, [random.randint(0, mod - 1) for _ in range(rows * cols)])

    @staticmethod
    def create_zero_message(mod, rows, cols): 
        """Create a zero message vector"""

        return Message(mod, rows, cols, [0 for _ in range(rows * cols)])

    @staticmethod
    def calculate_sample_error(bound, mod, rows, cols): 
        """Create a random error message vector"""

        return Message(mod, rows, cols, [sample_error(bound) % mod for _ in range(cols * rows)])
