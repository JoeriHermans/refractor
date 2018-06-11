class Plane:

    def __init__(self, z, shape):
        self._z = z
        self.shape = shape

    def set_redshift(self, z):
        self._z = z

    def get_redshift(self):
        return self._z
