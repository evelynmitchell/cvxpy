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

from affine_atom import AffAtom
from ...utilities import coefficient_utils as cu
import operator as op

class UnaryOperator(AffAtom):
    """
    Base class for expressions involving unary operators.
    """
    def __init__(self, expr):
        super(UnaryOperator, self).__init__(expr)

    def name(self):
        return self.OP_NAME + self.args[0].name()

    # Applies the unary operator to the value.
    def numeric(self, values):
        return self.OP_FUNC(values[0])

    # Returns the sign, curvature, and shape.
    def init_dcp_attr(self):
        self._dcp_attr = self.OP_FUNC(self.args[0]._dcp_attr)

    # Apply the unary operator to the argument.
    def graph_implementation(self, arg_objs):
        return (self.OP_FUNC(arg_objs[0]), [])

class NegExpression(UnaryOperator):
    OP_NAME = "-"
    OP_FUNC = op.neg

    def _tree_to_coeffs(self):
        """Return the dict of Variable to coefficient for the negation.
        """
        return cu.neg(self.args[0].coefficients())
