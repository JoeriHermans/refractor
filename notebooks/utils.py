"""
Simple utility methods for the notebooks in this folder.
"""

import PIL.Image

import numpy as np

import os


def load_image(path):
    image = PIL.Image.open(path)
    data = np.asarray(image.getdata()).reshape(image.size)

    return data
