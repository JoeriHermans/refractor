"""
"""

from astropy.constants import G
from astropy.constants import c

import astropy.units as u

import numpy as np

import torch

import torch.multiprocessing

import itertools



class Simulator:

    def __init__(self, cosmology, parallelism=10):
        self._cosmology = cosmology
        self._lens = None
        self._source = None
        self._distance_lens = None
        self._distance_lens_source = None
        self._distance_source = None
        self._thetas = None
        self._thetas_unit = None
        self._half_width_source = 0
        self._mpc_per_sourcepixel = 0.0
        self._parallelism = None
        self.set_parallelism(parallelism)

    def _initialize_planes(self):
        # Set the plane distances according to the cosmology.
        z_lens = self._lens.get_redshift()
        z_source = self._source.get_redshift()
        self._distance_lens = self._cosmology.angular_diameter_distance(z_lens)
        self._distance_source = self._cosmology.angular_diameter_distance(z_source)
        self._distance_lens_source = self._cosmology.angular_diameter_distance_z1z2(z_lens, z_source)
        # Compute several source characteristics.
        self._half_width_source = ((torch.tensor(self._source.shape, dtype=torch.float64)) - 1) / 2
        self._half_width_source = self._half_width_source.reshape(2, 1, 1)
        r_x, r_y = self._lens.get_angular_radius()
        r = r_x # Assume square field of view.
        source_shape = torch.tensor(self._source.shape, dtype=torch.float64)
        r = torch.tensor(r.to(u.rad).value, dtype=torch.float64)
        self._mpc_per_sourcepixel = (2 * torch.tan(r) *self._distance_source.value) / (source_shape - 1)
        self._mpc_per_sourcepixel = self._mpc_per_sourcepixel.reshape(-1, 1, 1)

    def _clear_planes(self):
        self._distance_lens = None
        self._distance_source = None
        self._distance_lens_source = None
        self._half_width_source = None
        self._mpc_per_sourcepixel = None

    def set_parallelism(self, num_tasks):
        self._parallelism = num_tasks
        torch.set_num_threads(num_tasks)

    def set_lens(self, lens):
        self._lens = lens
        self._initialize_planes()

    def get_lens(self):
        return self._plane_lens

    def set_source(self, source):
        self._source = source
        self._initialize_planes()

    def get_source(self):
        return self._plane_source

    def trace(self, lens, source):
        self._lens = lens
        self._source = source
        self._initialize_planes()
        lensed = torch.zeros(self._lens.shape, dtype=torch.float64)
        alphas = self._lens.get_alphas(self._cosmology)
        factor = (self._distance_lens_source / self._distance_source).value
        betas = self._lens.get_thetas() - factor * alphas
        # Obtain the pixel indexes.
        sources = ((torch.tan(betas) * self._distance_source.value) / self._mpc_per_sourcepixel) + self._half_width_source
        sources = sources.long().permute((2, 1, 0))
        # # Render the image.
        masked_indices = ((sources < 0) + (sources >= self._lens.shape[0])).sum(dim=2)
        for row in range(self._lens.shape[0]):
             for column in range(self._lens.shape[1]):
                 if masked_indices[row][column]:
                     continue
                 pixels = sources[row][column]
                 lensed[row][column] = self._source.data[pixels[0]][pixels[1]]
        # Clear the plane information.
        self._clear_planes()

        return lensed
