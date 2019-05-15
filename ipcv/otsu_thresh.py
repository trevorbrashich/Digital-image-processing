import ipcv
import numpy as np
import cv2
def w(im, k, maxCount = 255):

   hist = cv2.calcHist([im], [0], None, [maxCount+1], [0, maxCount+1])
   pdf = np.prod(np.shape(im))
   cdf = np.cumsum(pdf)
   histProb = hist/cdf
   return np.cumsum(histProb)[k]

def w0(im, k):
   w0calc = w(im, k)
   return w0calc

def w1(im, k):
   w1calc = 1 - (w(im, k))
   return w1calc

def mu(im, k, maxCount=255):

  # hist = cv2.calcHist([im], [0], None, [256], [0, 256])
  # histProb = hist / np.cumprod(np.shape(im))[-1]
   hist = cv2.calcHist([im], [0], None, [maxCount+1], [0, maxCount+1])
   pdf = np.prod(np.shape(im))
   cdf = np.cumsum(pdf)
   histProb = hist/cdf
   
   indiciesHist = np.arange(256)

   mean = indiciesHist * histProb
   r = np.cumsum(mean)[k]
   return r

def mu0(im, k, maxCount = 255):
   mu0calc =  (mu(im, k)) / (w(im, k))
   return mu0calc

def mu1(im, k, maxCount = 255):
   mu1calc =  ( mu(im, maxCount) - mu(im, k) ) / (1 - w(im, k))
   return mu1calc

def class_variance_b2(im, k, maxCount = 255):
    
   class_var = w0(im, k) * w1(im, k) * ( (mu1(im, k) - mu0(im, k))**2 )
   return class_var

def otsu_threshold(im, maxCount=255, verbose=False):

   hist = cv2.calcHist([im], [0], None, [maxCount+1], [0, maxCount+1])
   firstIndex = np.min(im)
   lastIndex = np.max(im)
   print(firstIndex) 
   print(lastIndex)
   r = np.zeros(maxCount+1)
   for i in range(65, 206):
      

   threshold = np.argmax(r)

   threshIm = np.ones(np.shape(im))
   threshIm = threshIm * im
   np.place(threshIm, im < threshold, 0)
   np.place(threshIm, im >= threshold, 1)

   return (threshIm, threshold)

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

