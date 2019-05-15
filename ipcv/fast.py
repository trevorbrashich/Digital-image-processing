import ipcv
import numpy as np
import cv2

def fast(src, differenceThreshold=50, contiguousThreshold=12, nonMaximalSuppression=True):
  
   circumference = 16
   radiusOffsets = [[-3,0],[-3,-1],[-2,-2],[-1,-3],
				  [0,-3],[1,-3],[2,-2],[3,-1],
				  [3,0],[3,1],[2,2],[1,3],
				  [0,3],[-1,3],[-2,2],[-3,1]]
   corners = np.zeros(src.shape)
   rows = src.shape[0]
   cols = src.shape [1]
   srcIm = src.copy()
   points = np.zeros((rows, cols, circumference))
   orig = np.zeros((rows, cols, circumference))

   for index,k in enumerate(radiusOffsets):
      points[:,:,index] = np.roll(np.roll(src, k[0], axis = 0), k[1], axis = 1)
      orig[:,:,index] = srcIm

   greater = (orig - points) > differenceThreshold
   less = (points - orig) > differenceThreshold
   
   mSum = corners
   checks = []
   for i in range(circumference):
      pOverlap = greater[:,:,0:contiguousThreshold] == 1
      nOverlap = less[:,:,0:contiguousThreshold] == 1
      pCheck = np.sum(pOverlap, axis=2)
      nCheck = np.sum(nOverlap, axis=2)

      corners[np.where(pCheck >= contiguousThreshold)] = 1
      corners[np.where(nCheck >= contiguousThreshold)] = 1

      mSum = mSum + corners
      greater = np.roll(greater,1,axis=2)
      less = np.roll(less,1,axis=2)

   finalCorners = np.clip(corners,0,1).astype(ipcv.IPCV_8U)
   return finalCorners

if __name__ == '__main__':

   import os.path
   import time
   import numpy
   import ipcv
   import cv2

   home = os.path.expanduser('~')
   filename = home + os.path.sep + 'src/python/examples/data/checkerboard.tif'
   filename = home + os.path.sep + \
              'src/python/examples/data/sparse_checkerboard.tif'

   src = cv2.imread(filename, cv2.IMREAD_UNCHANGED)

   startTime = time.time()
   dst = ipcv.fast(src, differenceThreshold=50,
                        contiguousThreshold=9,
                        nonMaximalSuppression=True)
   print('Elapsed time = {0} [s]'.format(time.time() - startTime))

   cv2.namedWindow(filename, cv2.WINDOW_AUTOSIZE)
   cv2.imshow(filename, src)

   if len(src.shape) == 2:
      annotatedImage = cv2.merge((src, src, src))
   else:
      annotatedImage = src
   annotatedImage[dst == 1] = [0,0,255]

   cv2.namedWindow(filename + ' (FAST Corners)', cv2.WINDOW_AUTOSIZE)
   cv2.imshow(filename + ' (FAST Corners)', annotatedImage)

   print('Corner coordinates ...')
   indices = numpy.where(dst == 1)
   numberCorners = len(indices[0])
   if numberCorners > 0:
      for corner in range(numberCorners):
         print('({0},{1})'.format(indices[0][corner], indices[1][corner]))

   action = ipcv.flush()

