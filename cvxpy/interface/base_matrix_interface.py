"""
Copyright 2013 Steven Diamond

This file is part of CVXPY.

CVXPY is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CVXPY is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CVXPY.  If not, see <http://www.gnu.org/licenses/>.
"""

import matrix_utilities as intf
import abc
import numbers
import numpy as np

class BaseMatrixInterface(object):
    """
    An interface between constants' internal values
    and the target matrix used internally.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def const_to_matrix(self, value, convert_scalars=False):
        """Convert an arbitrary value into a matrix of type self.target_matrix.

        Args:
            value: The constant to be converted.
            convert_scalars: Should scalars be converted?

        Returns:
            A matrix of type self.target_matrix or a scalar.
        """
        return NotImplemented

    # Adds a case for scalars to const_to_matrix methods.
    @staticmethod
    def scalar_const(converter):
        def new_converter(self, value, convert_scalars=False):
            if not convert_scalars and intf.is_scalar(value):
                return intf.scalar_value(value)
            else:
                return converter(self, value)
        return new_converter

    # Return an identity matrix.
    @abc.abstractmethod
    def identity(self, size):
        return NotImplemented

    # Return the dimensions of the matrix.
    @abc.abstractmethod
    def size(self, matrix):
        return NotImplemented

    # Get the matrix interpreted as a scalar.
    @abc.abstractmethod
    def scalar_value(self, matrix):
        return NotImplemented

    # Return a matrix with all 0's.
    def zeros(self, rows, cols):
        return self.scalar_matrix(0, rows, cols)

    # Return a matrix with all 1's.
    def ones(self, rows, cols):
        return self.scalar_matrix(1, rows, cols)

    # A matrix with all entries equal to the given scalar value.
    @abc.abstractmethod
    def scalar_matrix(self, value, rows, cols):
        return NotImplemented

    # Return the value at the given index in the matrix.
    def index(self, matrix, key):
        value = matrix[key]
        # Reduce to a scalar if possible.
        if intf.size(value) == (1,1):
            return intf.scalar_value(value)
        else:
            return value

    # Coerce the matrix into the given shape.
    @abc.abstractmethod
    def reshape(self, matrix, size):
        return NotImplemented

    # Add the block to the matrix at the given offset.
    def block_add(self, matrix, block, vert_offset, horiz_offset, rows, cols,
                  vert_step=1, horiz_step=1):
        # If the block is a scalar, promote it.
        if intf.is_scalar(block):
            block = self.scalar_matrix(intf.scalar_value(block), rows, cols)
        # If the block is a vector coerced into a matrix, promote it.
        elif intf.is_vector(block) and cols > 1:
            block = self.reshape(block, (rows, cols))
        # If the block is a matrix coerced into a vector, vectorize it.
        elif not intf.is_vector(block) and cols == 1:
            block = self.reshape(block, (rows, cols))
        # Ensure the block is the same type as the matrix.
        elif type(block) != type(matrix):
            block = self.const_to_matrix(block)
        matrix[vert_offset:(rows+vert_offset):vert_step,
               horiz_offset:(horiz_offset+cols):horiz_step] += block