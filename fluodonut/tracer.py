"""
`fluodonut` raytracer logic.
"""

from astropy.constants import G
from astropy.constants import c

import astropy.units as c

import numpy as np



class PlaneTracer:
    """
    TODO
    """

    def __init__(self, cosmology, axial_radius_x, axial_radius_y):
        self._axial_radius_x = axial_radius_x
        self._axial_radius_y = axial_radius_y
        self._cosmology = cosmology
        self._lens = None
        self._source = None

    def set_lens(self, lens):
        self._lens = lens

    def get_lens(self):
        return self._lens

    def set_source(self, source):
        self._source = source

    def get_source(self):
        return self._source

    def trace(self, threads=1):
        image = np.zeros(self._lens[0].shape)

        # Compute the bending angles of all lenses.
        self._compute_alphas()
        # Compute the source target (beta).
        self._compute_sources()

        return image
