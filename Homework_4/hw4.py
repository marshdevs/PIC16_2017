# Homework 4
# Filename: hw4.py
# Author: Marshall Briggs

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
matplotlib.use('TkAgg')

def heart(img):
    """
    Function: heart(img)
    INPUT: An image, img
    OUTPUT: A heart shaped cutout of the image on a pink background.
    Definition: a function that takes an image as input, and outputs 
                a heart-shaped cut-out of it on a pink background.
    """
    img = mpimg.imread('steve.jpg')
    plt.imshow(img)
    plt.show()
