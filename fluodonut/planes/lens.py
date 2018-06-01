"""
A lensing class which provides the basic functionality and properties
of a gravitational lens.
"""

import fluodonut.planes.Plane

import numpy as np



class Lens(fluodonut.planes.Plane):

    def __init__(self, data, z):
        super(Lens, self).__init__(data, z)
        self._alphas = np.zeros(self.get_shape())

    def _compute_alphas(self):
        raise NotImplementedError

    def get_alphas(self):
        return self._alphas

    def get_mass(self):
        raise NotImplementedError
