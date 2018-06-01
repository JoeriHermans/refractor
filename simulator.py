from astropy.constants import G
from astropy.constants import c
from astropy.cosmology import WMAP9 as cosmology

from random import random as rand

import astropy.constants
import astropy.cosmology
import astropy.units as u

import matplotlib.pyplot as plt

import PIL.Image

import multiprocessing

import numpy as np

import random

import os


def main():
    data_path = "data/"
    source_paths = [data_path + source_name for source_name in os.listdir(data_path)]
    num_sources = len(source_paths)
    num_simulations = 1
    for trial in range(num_simulations):
        simulate(source_paths[int(rand() * num_sources)])
        #simulate(source_paths[0])


def load_source(path):
    image = PIL.Image.open(path)
    data = np.asarray(image.getdata()).reshape(image.size)

    return data


def normalize(v):
    return v / np.linalg.norm(v)


def simulate(source_path):
    # Set the lens parameters.
    z_lens = 0.5
    z_source = 2.0
    d_lens = cosmology.angular_diameter_distance(z_lens)
    d_source = cosmology.angular_diameter_distance(z_source)
    d_lens_source = cosmology.angular_diameter_distance_z1z2(z_lens, z_source)
    source_image = load_source(source_path)
    lens_image = np.zeros(source_image.shape)
    lens_potential = np.zeros(source_image.shape)
    lens_position = np.array([0, 0]) * u.arcsec # Position from the center.
    lens_mass = (1 * 1000000000000 * u.M_sun).to(u.kg)
    alpha = np.zeros((source_image.shape[0], source_image.shape[1], 2))
    magnification = np.zeros((source_image.shape[0], source_image.shape[1], 4))
    angular_axial_radius = 10 * u.arcsec
    angular_axial_diameter = 2 * angular_axial_radius
    half_width_x = (source_image.shape[0] - 1) / 2
    half_width_y = (source_image.shape[0] - 1) / 2
    angle_edge = np.sqrt(angular_axial_diameter ** 2 + angular_axial_diameter ** 2).to(u.rad)
    arcsec_per_pixel_x = (angular_axial_diameter * u.arcsec) / source_image.shape[0]
    arcsec_per_pixel_y = (angular_axial_diameter * u.arcsec) / source_image.shape[1]
    mpc_per_lenspixel_x = 2 * (np.tan(angular_axial_radius) * d_lens) / source_image.shape[0]
    mpc_per_lenspixel_y = 2 * (np.tan(angular_axial_radius) * d_lens) / source_image.shape[1]
    mpc_per_lenspixel = (np.tan(angle_edge) * d_lens) / source_image.shape[0]
    mpc_per_sourcepixel_x = 2 * (np.tan(angular_axial_radius) * d_source) / source_image.shape[0]
    mpc_per_sourcepixel_y = 2 * (np.tan(angular_axial_radius) * d_source) / source_image.shape[1]
    mpc_per_sourcepixel = (np.tan(angle_edge) * d_source) / source_image.shape[1]
    # Flip the source image to have a consistent x-axis.
    source_image = np.flip(source_image, 0)
    # Start raytracing for every pixel in the lens / image plane.
    for row in range(lens_image.shape[0]):
        for column in range(lens_image.shape[1]):
            # Compute the angle to the lens plage in arcseconds.
            x = column - half_width_x
            y = row - half_width_y
            b_x = mpc_per_lenspixel_x * x
            b_y = mpc_per_lenspixel_y * y
            b = np.array([b_x.value, b_y.value]) * u.Mpc
            r = np.linalg.norm(b, ord=2) * u.Mpc
            alpha_approx = (4 * G * lens_mass) / (c ** 2 * r.to(u.m))
            alpha = (d_lens_source / d_source) * alpha_approx * u.rad
            theta_x = np.arctan2(b_x, d_lens)
            theta_y = np.arctan2(b_y, d_lens)
            theta = np.array([theta_x.value, theta_y.value]) * u.rad
            beta = theta.value - normalize(theta.value) * alpha.value
            lens_potential[row][column] = np.mean(alpha.value)
            source = (np.tan(beta) * d_source) / mpc_per_sourcepixel_x + half_width_x
            source = np.rint(source).astype(int)
            if np.any(source < 0) or np.any(source >= source_image.shape[0]):
                continue
            lens_image[row][column] = source_image[source[0]][source[1]]
    f, (ax1, ax2) = plt.subplots(ncols=2)
    ax1.imshow(source_image)
    ax2.imshow(np.rot90(np.flip(lens_image, 1)))
    plt.show()


if __name__ == '__main__':
    main()
