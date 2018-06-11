import refractor.plane

import astropy.units as u

import torch

from astropy.constants import G
from astropy.constants import c



class BaseLens(refractor.plane):

    def __init__(self, z, shape, r_x=1 * u.arcsec, r_y=1 * u.arcsec):
        super(BaseLens, self).__init__(z, shape)
        self._angular_radius_x = r_x
        self._angular_radius_y = r_y

    def get_alphas(self, thetas, cosmology):
        raise NotImplementedError

    def get_angular_radius(self):
        return self._angular_radius_x, self._angular_radius_y



class PointMassLens(BaseLens):

    def __init__(self, z, shape, mass, r_x=1 * u.arcsec, r_y=1 * u.arcsec):
        super(PointMassLens, self).__init__(z, shape, r_x, r_y)
        self._mass = mass.to(u.kg)

    def get_alphas(self, thetas, cosmology):
        distance_lens = cosmology.angular_diameter_distance(self._z).value
        radi = torch.norm(torch.tan(thetas) * distance_lens, p=2, dim=0) * 3.08567758128e+22
        alphas = (4 * G.value * self._mass.value) / (c.value ** 2 * radi)

        return alphas
