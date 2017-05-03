import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.image as mpimg

# Salt & Pepper noise:
#   Each pixel will be replaced by white, with probability wp,
#   or with black, with probability pb. Creates this kind of "Grainy noise"
#   that you would see on old black & white TVs.

# Gaussian noise:
#   For each pixel, add some noise with a gaussian distribution
#   np.random.normal(mu = mean, sigma = sd, [n,m]) returns an n*m
#   array of samples from the normal distribution
#   im.shape gives the dimensions of the image

def salt_pepper(im,ps=.1,pp=.1):
    im1=im[:,:,0].copy()
    n,m=im1.shape
    for i in range(n):
        for j in range(m):
            b=np.random.uniform()
            if b<ps:
                im1[i,j]=0
            elif b>1-pp:
                im1[i,j]=1
    noisy_im=[[[im1[i,j]]*3 for j in range(m)] for i in range(n)]
    return noisy_im        


def gauss_noise(im,p=1/4):
    im1=im[:,:,0].copy()
    n,m=im1.shape
    #generate a noise matrix with mean 0 and std sigma*p
    noise=np.random.normal(0,np.var(im1)**(1/2)*p,[n,m])
    noisy_im1=im1+noise
    for i in range(n):
        for j in range(m):
            if noisy_im1[i,j]>1:
                noisy_im1[i,j]=1
            elif noisy_im1[i,j]<0:
                noisy_im1[i,j]=0
    noisy_im=[[[noisy_im1[i,j]]*3 for j in range(m)] for i in range(n)]
    return noisy_im
    
def main():
    img=mpimg.imread('IMG_6176.JPG')
    noise = salt_pepper(img)
    #noise = gauss_noise(img)
    plt.imshow(img)