"""
   title:: 
      otsu_threshold

   description::
      this method performs otsu thresholding to an image by finding a threshold value
      that seperates the background and foreground elements in a grayscale image given
      otsu's equations. The method the sets all values to either 0 or 1 based on whether 
      the dc value lies above or below the threshold value
   
   attributes::
      image - image being thresholded
      maxCount - the max DC value of the image
      verbose - graphing the pdf and the vertical threshold value
  returns::
      threshold, image 
   author::
      Trevor Brashich
"""

import cv2
import ipcv
import numpy as np
import matplotlib.pyplot
import matplotlib

def otsu_threshold(im, maxCount=255, verbose=False):

   #error checking
   if (not isinstance(im, np.ndarray)):
      raise TypeError("image is not a numpy ndarray; use openCV's imread")
   
   if (len(np.shape(im)) != 2):
      raise ValueError("Shape of image is not a grayscale image or histogram")
    
   #creates histogram, pdf and cdf of the image 
   h = cv2.calcHist([im], [0], None, [maxCount+1], [0, maxCount+1])
   pdf = h / np.prod(np.shape(im))
   cdf = np.cumsum(pdf)
 
   #finds max and min values of dc values in image
   minDC = np.min(im)
   maxDC = np.max(im)

   #creates a pdf and cdf within the range of non-zero dc values
   p = pdf[minDC:maxDC]
   c = cdf[minDC:maxDC]
 
   # performs otsu's method

   omega = c
   rangeDC = ((maxDC) - minDC)
   # creates an empty array of range from minDc to maxDC
   mu = np.zeros(rangeDC)
   muSum = 0
   DC = np.array(range(minDC, maxDC+1))
 
   # indexes the probability * the dc value at each dc in range and sums them
   for i in range(0, rangeDC):
      muSum += p[i]*DC[i] 
      mu[i] = muSum
   
   # finds the last value of mu
   muT = mu[-1] 
   
   #calculates sigma(k) based on early equations found
   sigmatop = (((muT*omega) - mu)**2) 
   sigmabot = (omega * (1 - omega))
   sigmaK = (sigmatop / sigmabot)
   
   #threshold is the max value of the sigma
   # because we indexed from the minDC it has to be added to 
   # the threshold to be in range from 0-255
   threshold = np.argmax(sigmaK) + minDC 
 
   im = im.copy()
   #scales dc values above threshold to 1 and below to 0
   im[im <= threshold] = 0
   im[im > threshold] = 1
   
   im = im.astype(np.uint8)
   
   #plots the pdf and threshold line
   if (verbose == True):
      Max = range(256)
      matplotlib.pyplot.subplot(1, 1, 1)
      matplotlib.pyplot.ylabel('pdf')
      matplotlib.pyplot.xlabel('Digital Count')
      matplotlib.pyplot.xlim([0,256])
      matplotlib.pyplot.axvline(threshold, color ='g')
      matplotlib.pyplot.plot(Max, pdf, color = 'black')          
      matplotlib.pyplot.show()
   return im, threshold
 

if __name__ == '__main__':

   import cv2
   import ipcv
   import os.path
   import time

   home = os.path.expanduser('~')
   filename = home + os.path.sep + 'src/python/examples/data/giza.jpg'

   im = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
   print('Filename = {0}'.format(filename))
   print('Data type = {0}'.format(type(im)))
   print('Image shape = {0}'.format(im.shape))
   print('Image size = {0}'.format(im.size))

   startTime = time.time()
   thresholdedImage, threshold = ipcv.otsu_threshold(im, verbose=True)
   print('Elapsed time = {0} [s]'.format(time.time() - startTime))

   print('Threshold = {0}'.format(threshold))

   cv2.namedWindow(filename, cv2.WINDOW_AUTOSIZE)
   cv2.imshow(filename, im)
   cv2.namedWindow(filename + ' (Thresholded)', cv2.WINDOW_AUTOSIZE)
   cv2.imshow(filename + ' (Thresholded)', thresholdedImage * 255)

   action = ipcv.flush()

