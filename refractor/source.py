import refractor



class Source(refractor.plane):

    def __init__(self, z, data):
        super(Source, self).__init__(z, data.shape)
        self.data = data
