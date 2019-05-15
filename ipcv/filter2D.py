import ipcv
import numpy as np
import cv2

def filter2D(src, dstDepth, kernel, delta=0, maxCount=255):

    
   dstOut = np.zeros(src.shape)
  # kernelflat = kernel.flatten()
   rows = kernel.shape[0] // 2
   cols = kernel.shape[1] // 2
   kernelW = np.sum(kernel)
   kernel = kernel / kernelW
   kernelflat = kernel.flatten()

  # print(rows, cols)
  # print(kernelflat)

  # for rows in range(0, rows):
  #    for cols in range(0, cols):   
  #       dst = (src * kernel[rows, cols])    
  #       src = np.roll(src, (rows, cols), (0, 1))
  #       dstOut += dst
  
   for i in range(0, kernel.size):
      srcIm = np.roll(src, -1, i %2)
      srcIm = srcIm.astype(dstDepth)
      dstOut += (srcIm * kernelflat[i])


 #  dstOut = dstOut / np.sum(np.abs(kernel))  
   dstOut += delta
   dstOut = np.clip(dstOut, 0, maxCount)
   dstOut = dstOut.astype(dstDepth)
   return dstOut

if __name__ == '__main__':

   import cv2
   import os.path
   import time
   import numpy
  
   home = os.path.expanduser('~')
   filename = home + os.path.sep + 'src/python/examples/data/redhat.ppm'
   filename = home + os.path.sep + 'src/python/examples/data/crowd.jpg'
   filename = home + os.path.sep + 'src/python/examples/data/checkerboard.tif'
   filename = home + os.path.sep + 'src/python/examples/data/lenna.tif'

   src = cv2.imread(filename, cv2.IMREAD_UNCHANGED)

   dstDepth = ipcv.IPCV_8U
   #kernel = numpy.asarray([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
  # offset = 0
  # kernel = numpy.asarray([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])
  # offset = 128
  # kernel = numpy.ones((15,15))
  # offset = 0
   kernel = numpy.asarray([[1,1,1],[1,1,1],[1,1,1]])
   offset = 0

   startTime = time.time()
   dst = ipcv.filter2D(src, dstDepth, kernel, delta=offset)
   print('Elapsed time = {0} [s]'.format(time.time() - startTime))

   cv2.namedWindow(filename, cv2.WINDOW_AUTOSIZE)
   cv2.imshow(filename, src)

   cv2.namedWindow(filename + ' (Filtered)', cv2.WINDOW_AUTOSIZE)
   cv2.imshow(filename + ' (Filtered)', dst)

   action = ipcv.flush()

