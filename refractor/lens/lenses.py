import refractor.plane

import astropy.units as u

import torch

import numpy as np

from astropy.constants import G
from astropy.constants import c



class BaseLens(refractor.plane):

    def __init__(self, z, shape, r_x=1 * u.arcsec, r_y=1 * u.arcsec):
        super(BaseLens, self).__init__(z, shape)
        self._angular_radius_x = r_x
        self._angular_radius_y = r_y
        self._thetas = None
        self._thetas_unit = None
        self._generate_thetas()

    def _generate_thetas(self):
        # Obtain the axial angular radius of the lens plane in arcseconds.
        axes_x = np.linspace(-self._angular_radius_x, self._angular_radius_x, self.shape[0])
        axes_y = np.linspace(-self._angular_radius_y, self._angular_radius_y, self.shape[1])
        # Convert to radians.
        axes_x = axes_x.to(u.rad)
        axes_y = axes_y.to(u.rad)
        # Pre-allocate the rays and unit-rays of the ray-tracer.
        xx, yy = np.meshgrid(axes_x, axes_y)
        self._thetas = torch.tensor(np.array([xx, yy]), dtype=torch.float64)
        self._thetas_unit = self._thetas / torch.norm(self._thetas, p=2, dim=0)

    def get_thetas(self):
        return self._thetas

    def get_unit_thetas(self):
        return self._thetas_unit

    def get_alphas(self, cosmology, normalize=True):
        raise NotImplementedError

    def get_angular_radius(self):
        return self._angular_radius_x, self._angular_radius_y



class PointMassLens(BaseLens):

    def __init__(self, z, shape, mass, r_x=1 * u.arcsec, r_y=1 * u.arcsec, pos=(0., 0.) * u.arcsec):
        super(PointMassLens, self).__init__(z, shape, r_x, r_y)
        self._mass = mass.to(u.kg)
        self._pos_angles = torch.tensor(pos.to(u.rad), dtype=torch.float64)

    def get_mass(self):
        return self._mass

    def get_alphas(self, cosmology, normalize=True):
        distance_lens = cosmology.angular_diameter_distance(self._z).value
        radi = torch.norm(torch.tan(self._thetas) * distance_lens, p=2, dim=0) * 3.08567758128e+22
        alphas_approx = (4 * G.value * self._mass.value) / (c.value ** 2 * radi)
        if normalize:
            alphas = alphas_approx * self._thetas_unit
        else:
            alphas = alphas_approx

        return alphas
