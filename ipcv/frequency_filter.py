import cv2
import ipcv
import numpy as np
def frequency_filter(im, frequencyFilter, delta=0):

   rows = im.shape[0]
   cols = im.shape[1]
   bands = im.shape[2] 
   filteredIm = np.zeros((rows, cols, bands))
   for band in range(bands):
      imTransform = np.fft.fft2(im[:,:,band])
      centered = np.fft.fftshift(imTransform)
      filterTransform = centered * frequencyFilter
      uncentered = np.fft.ifftshift(filterTransform)
      filteredIm[:,:,band] = np.fft.ifft2(uncentered)
   filteredIm += delta

   return filteredIm.astype(np.complex128)

if __name__ == '__main__':

   import cv2
   import ipcv
   import numpy
   import os.path
   import time

   home = os.path.expanduser('~')
   filename = home + os.path.sep + 'src/python/examples/data/lenna.tif'
   filename = home + os.path.sep + 'src/python/examples/data/giza.jpg'

   im = cv2.imread(filename)

   frequencyFilter = ipcv.filter_lowpass(im, 
                                         16, 
                                         filterShape=ipcv.IPCV_GAUSSIAN)

   startTime = time.clock()
   offset = 0
   filteredImage = ipcv.frequency_filter(im, frequencyFilter, delta=offset)
   filteredImage = numpy.abs(filteredImage)
   filteredImage = filteredImage.astype(dtype=numpy.uint8)
   elapsedTime = time.clock() - startTime
   print('Elapsed time (frequency_filter)= {0} [s]'.format(elapsedTime))

   cv2.namedWindow(filename, cv2.WINDOW_AUTOSIZE)
   cv2.imshow(filename, im)
   cv2.imshow(filename, ipcv.histogram_enhancement(im))

   filterName = 'Filtered (' + filename + ')'
   cv2.namedWindow(filterName, cv2.WINDOW_AUTOSIZE)
   cv2.imshow(filterName, filteredImage)
   cv2.imshow(filterName, ipcv.histogram_enhancement(filteredImage))

   ipcv.flush()
