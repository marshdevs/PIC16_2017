# -*- coding: utf-8 -*-
"""
Write a function that takes as input a gray-scale image. For convenience, we assume that the image
takes the form of an n × m numpy array, where each pixel is represented by a single real number
between 0 and 1, representing the gray scale from black to white.
Your function darkens only the top half of the image a little. You can let the amount of darkening be
a parameter of your function.
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

def darken_top_half(im, d):
    im1=im[:,:,0].copy()
    n,m=im1.shape
    
    x,y=np.ogrid[0:n, 0:m]
    manipimg = im.copy()
    manipimg = [[d if b <n/2 else im1[a,b] for b in range(m)] for a in range(n)]  
    plt.imshow(manipimg, gray)
    plt.show()
    
def main():
    img = mpimg.imread('steve.jpg')
    darken_top_half(img, 1)
    
if __name__ == "__main__": main()