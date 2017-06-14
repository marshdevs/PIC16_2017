# Homework 4
# Filename: hw4.py
# Author: Marshall Briggs

# import matplotlib
# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import math

def normalizeImage(im):
  """
  Helper function from the TA

  Renormalize an image read in by matplotplib.pyplot.imread.

  The returned image will have pixel data in the range [0,1], even if the input
  image used the range [0,255] instead.

  NOT FULLY TESTED; USE AT YOUR OWN RISK!
  """

  if im.dtype == np.uint8:
    # 8-bit integer pixel data; convert to float and rescale
    return im.astype(np.float32) / 255.0
  elif im.dtype == np.float32 or im.dtype == np.float64:
    # Floating-point data; make a copy for consistency
    return im.copy()
  else:
    raise ValueError("Unrecognized data type: %s" % im.dtype)

def heart(im):
    """
    Function: heart(img)
    INPUT: An image, img
    OUTPUT: A heart shaped cutout of the image on a pink background.
    Definition: a function that takes an image as input, and outputs 
                a heart-shaped cut-out of it on a pink background.
    """
    img = normalizeImage(im)
    im1=img[:,:,0].copy()
    n,m=im1.shape
    im2 = im1.copy()

    imask=[[[0,0,1]]*m]*n
    imask=np.array(imask,dtype='float')
    x,y=np.ogrid[0:n, 0:m]
    # secondterm = ((x-n/2)**2) * ((y-m/2)**3)
    # heartmask= ((x-n/2)**2+(y-m/2)**2 - 1)**3 - secondterm < 0

    heartmask = ((x-n/5)**2 + (y-m/3)**2 > 16000) & ((x-n/5)**2 + (y-2*m/3)**2 > 16000) | ( (y < 2*x - n/4) | (y > -2*x + 3*n/4) )
    # rcircmask = ((x-n/5)**2 + (y-2*m/3)**2 > 16000) & (x < n/4)
    im2[heartmask] = 1
    # & (y < 2*m/3 + 400) & (y > x)
    # rlinemask = (y > m/3 + 500) & (y < 2*m/3 + 400) & (y > -x)
    # bwim = [[[im2[i,j]]*3 for j in range(m)] for i in range(n)]
    plt.imshow(im2, cmap='gray')
    plt.show()

def blurring(im, method):
    """
    Function: blurring(im, method)
    INPUT: Image, string method option
    OUTPUT: The "original" image, blurred with the desired option
    Description: A function that takes a gray-scale picture, and offers 
                 two options for noise removal: uniform or gaussian
    """
    if method == 'uniform':
        im1 = normalizeImage(im)
        k = 5
        blurr = np.array([[0.04 for _ in range(k)] for _ in range(k)])
        n,m=im1.shape
        blurredim1 = im1.copy()
        for i in range(n):
            for j in range(m):
                if i > 2 and i < (n-2) and j > 2 and j < (m-2):
                    nlist = [[im1[a,b] for a in range(i-2, i+3)] for b in range(j-2, j+3)]
                    neighbors = np.array(nlist)
                    averages = neighbors*blurr
                    newpixel = np.sum(averages)
                    blurredim1[i,j] = newpixel
        # plt.imshow(im1)
        plt.imshow(blurredim1, cmap="gray", norm=plt.Normalize(vmin=0.0, vmax=1.0))
        plt.show()

    elif method == 'gaussian':
        img = normalizeImage(im)
        im1=img[:,:,0].copy()
        k = 5
        s = 1

        blurr = np.array([[(1.0/2.0*math.pi*float(s)**2)*math.e**(-((float(o)-(float(k)-1.0)/2.0)**2 + (float(p)-(float(k)-1.0)/2.0)**2)/2.0*float(s)**2) for o in range(k)] for p in range(k)])
        n,m=im1.shape
        blurredim1 = im1.copy()
        for i in range(n):
            for j in range(m):
                if i > 2 and i < (n-2) and j > 2 and j < (m-2):
                    nlist = [[im1[a,b] for a in range(i-2, i+3)] for b in range(j-2, j+3)]
                    neighbors = np.array(nlist)
                    # print neighbors
                    averages = neighbors*blurr
                    # print averages
                    newpixel = np.sum(averages)
                    blurredim1[i,j] = newpixel
        # noisy_im=[[[blurredim1[i,j]]*3 for j in range(m)] for i in range(n)]
        plt.imshow(blurredim1, cmap="gray")
        # plt.imshow(blurredim1, cmap="gray", norm=plt.Normalize(vmin=0.0, vmax=1.0))
        plt.show()
    else:
        print "Invalid method specified."

def detect_edge(im, method):
    """
    Function: detect_edge(im, method)
    INPUT: An image, im, edge detection method option
    OUTPUT: The input image, with specified edges highlighted
    Description: A function that takes a gray-scale image and detects edges,
                 with the option of horizontal, vertical or both
    """
    img = normalizeImage(im)
    im1=img[:,:,0].copy()
    n,m=im1.shape
    edgedim1 = im1.copy()
    if method == "horizontal":
        for i in range(n):
            for j in range(m):
                if i > 1 and i < (n-1) and j > 1 and j < (m-1):
                    hsfilter = np.array([[-1.0,0,1.0],[-2.0,0,2.0],[-1.0,0,1.0]])
                    nlist = [[im1[a,b] for a in range(i-1, i+2)] for b in range(j-1, j+2)]
                    sh = hsfilter*nlist
                    newpixel = np.sum(sh)
                    edgedim1[i,j] = (newpixel + 4.0)/8.0
        plt.imshow(edgedim1, cmap="gray")
        plt.show()

    elif method == "vertical":
        for i in range(n):
            for j in range(m):
                if i > 1 and i < (n-1) and j > 1 and j < (m-1):
                    vsfilter = np.array([[-1.0,-2.0,-1.0],[0,0,0],[1.0,2.0,1.0]])
                    nlist = [[im1[a,b] for a in range(i-1, i+2)] for b in range(j-1, j+2)]
                    sv = vsfilter*nlist
                    newpixel = np.sum(sv)
                    edgedim1[i,j] = (newpixel + 4.0)/8.0
        plt.imshow(edgedim1, cmap="gray")
        plt.show()
    elif method == "both":
        for i in range(n):
            for j in range(m):
                if i > 1 and i < (n-1) and j > 1 and j < (m-1):
                    hsfilter = np.array([[-1.0,0,1.0],[-2.0,0,2.0],[-1.0,0,1.0]])
                    vsfilter = np.array([[-1.0,-2.0,-1.0],[0,0,0],[1.0,2.0,1.0]])
                    nlist = [[im1[a,b] for a in range(i-1, i+2)] for b in range(j-1, j+2)]
                    sh = hsfilter*nlist
                    sv = vsfilter*nlist
                    newpixel = math.sqrt((np.sum(sh)**2 + np.sum(sv)**2))
                    edgedim1[i,j] = 2 * math.fabs((newpixel + 4.0)/8.0 - 0.5)
        plt.imshow(edgedim1, cmap="gray")
        plt.show()
    else:
        print "Invalid method specified."

def otsu_threshold(im):
    """
    Function: otsu_threshold(im)
    INPUT: An image
    OUTPUT: The input image, divided into foreground (white) and background (black)
    Description: A function that splits a gray-scale image into foreground and 
                 background using Otsu's thresholding method
    """
    img = normalizeImage(im)
    im1=img[:,:,0].copy()

    n,m=im1.shape
    fgbgim1 = im1.copy()
    bag=np.sort(im1.reshape([n*m, 1]))
    mu = np.mean(bag[:])
    maxBG = 0
    optT = 0
    possibleT = [0.001*a for a in range(1000)]

    for t in possibleT:
        ind = np.argmax(bag>t)
        weightFG  = ind / float(n*m)
        muFG = np.mean(bag[:ind])
        weightBG = (float(n*m) - ind)/ float(n*m)
        muBG = np.mean(bag[ind:])
        rt = weightFG*((muFG - mu)**2) + weightBG*((muBG - mu)**2)
        if rt > maxBG:
            maxBG = rt
            optT = ind

    fgmask = im1<=bag[optT]
    bgmask = im1>bag[optT]
    fgbgim1[fgmask] = 0
    fgbgim1[bgmask] = 1
    plt.imshow(fgbgim1, cmap="gray")
    plt.show()

def blur_background(im):
    """
    Function: blur_background(im)
    INPUT: An image, im
    OUTPUT: The input image, split into foreground, and background (blurred)
    Description: A function that combines the second and fourth challenges, by 
                 identifying the background of an image, and blurring it
    """
    img = normalizeImage(im)
    im1=img[:,:,0].copy()

    n,m=im1.shape
    fgbgim1 = im1.copy()
    bag=np.sort(im1.reshape([n*m, 1]))
    mu = np.mean(bag[:])
    maxBG = 0
    optT = 0
    possibleT = [0.001*a for a in range(1000)]

    for t in possibleT:
        ind = np.argmax(bag>t)
        weightFG  = ind / float(n*m)
        muFG = np.mean(bag[:ind])
        weightBG = (float(n*m) - ind)/ float(n*m)
        muBG = np.mean(bag[ind:])
        rt = weightFG*((muFG - mu)**2) + weightBG*((muBG - mu)**2)
        if rt > maxBG:
            maxBG = rt
            optT = ind

    fgmask = im1>bag[optT]
    bgmask = im1<=bag[optT]

    fgbgim1[fgmask] = mu

    fgbgim2 = fgbgim1.copy()


    k = 9
    blurr = np.array([[0.011 for _ in range(k)] for _ in range(k)])
    for i in range(n):
        for j in range(m):
            if i > 4 and i < (n-4) and j > 4 and j < (m-4):
                nlist = [[fgbgim1[a,b] for a in range(i-4, i+5)] for b in range(j-4, j+5)]
                neighbors = np.array(nlist)
                averages = neighbors*blurr
                newpixel = np.sum(averages)
                fgbgim2[i,j] = newpixel
    
    fgbgim3 = [[im1[i,j] if fgmask[i,j] else fgbgim2[i,j] for j in range(m)] for i in range(n)]
    plt.imshow(fgbgim3, cmap='gray')
    plt.show()

def main():
    # Test Case for Challenge 1 - Finish later
    # img = mpimg.imread('steve.jpg')
    # heart(img)

    # Test Cases for Challenge 2 - Finished?
    # img = mpimg.imread('uniform_noise.jpg')
    # blurring(img, 'uniform')
    # img = mpimg.imread('gaussian_noise.jpg')
    # blurring(img, 'gaussian')

    # Test Cases for Challenge 3 - Finished?
    # img = mpimg.imread('edges.png')
    # detect_edge(img, 'horizontal')
    # detect_edge(img, 'vertical')
    # detect_edge(img, 'both')

    # Test Cases for Challenge 4 - Finished?
    #  img = mpimg.imread('husky.jpg')
    #  otsu_threshold(img)

    # Test Cases for Challenge 5 - Finished?
    # img = mpimg.imread('husky.jpg')
    # blur_background(img)
    return


if __name__ == "__main__": main()