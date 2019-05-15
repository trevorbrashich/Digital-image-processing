import numpy as np
import math
import cv2
import ipcv

def harris(src, sigma=1, k=0.04):

   srcDtype = src.dtype
   src = src.astype(np.float64)

   k1 = np.array([-1, 0, 1])
   k2 = np.array([-1, 0, 1]).reshape(1,3)
   pDerX = cv2.filter2D(src, -1, k1) 
   pDerY = cv2.filter2D(src, -1, k2) 

   A = pDerX**2
   B = pDerY**2
   C = pDerX * pDerY

   kX = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
   #kY = np.flip(np.rot90(kX), 0)
   kY = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
   kernel = np.exp(-0.5 *(((kX**2)+(kY**2))/(sigma**2)))

   A = cv2.filter2D(A, -1, kernel)
   B = cv2.filter2D(B, -1, kernel)
   C = cv2.filter2D(C, -1, kernel)

   tr = A + B
   det = (A * B) - C**2
   r = det - k*(tr**2)
   return r

if __name__ == '__main__':

   import cv2
   import ipcv
   import os.path
   import time
   import numpy

   home = os.path.expanduser('~')
   filename = home + os.path.sep + 'src/python/examples/data/checkerboard.tif'
   filename = home + os.path.sep + \
              'src/python/examples/data/sparse_checkerboard.tif'

   src = cv2.imread(filename, cv2.IMREAD_UNCHANGED)

   sigma = 1
   k = 0.04
   startTime = time.time()
   dst = ipcv.harris(src, sigma, k)
   print('Elapsed time = {0} [s]'.format(time.time() - startTime))

   cv2.namedWindow(filename, cv2.WINDOW_AUTOSIZE)
   cv2.imshow(filename, src)

   if len(src.shape) == 2:
      annotatedImage = cv2.merge((src, src, src))
   else:
      annotatedImage = src
   fractionMaxResponse = 0.25
   annotatedImage[dst > fractionMaxResponse*dst.max()] = [0,0,255]

   cv2.namedWindow(filename + ' (Harris Corners)', cv2.WINDOW_AUTOSIZE)
   cv2.imshow(filename + ' (Harris Corners)', annotatedImage)

   print('Corner coordinates ...')
   indices = numpy.where(dst > fractionMaxResponse*dst.max())
   numberCorners = len(indices[0])
   if numberCorners > 0:
      for corner in range(numberCorners):
         print('({0},{1})'.format(indices[0][corner], indices[1][corner]))

   action = ipcv.flush()

