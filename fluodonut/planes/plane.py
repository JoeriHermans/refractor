"""
Abstract plane class.

Describes the general properties and actions of a plane in a lensing system.
"""


class Plane:

    def __init__(self, data, z=None):
        self._data = data
        self._z = z

    def get_shape(self):
        return self._data.shape

    def set_z(self, z):
        self._z = z

    def get_z(zelf):
        return self._z

    def set_redshift(self, redshift):
        self.set_z(redshift)

    def get_redshift(self):
        return self._z

    def __getitem__(self, index):
        return self._data[index]
