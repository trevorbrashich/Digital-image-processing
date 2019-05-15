import cv2
import ipcv
import numpy as np
import math
def bilateral_filter(src,
                     sigmaDistance,
                     sigmaRange,
                     d=-1,
                     borderType=ipcv.BORDER_WRAP,
                     maxCount=255):

   dst = np.zeros(src.shape)
   cweight = []
   sweight = []
   e = math.e

   sizec = 

   for row in range(src.shape[0]):
      for col in range(src.shape[1]):
          


if __name__ == '__main__':

   import cv2
   import ipcv
   import os.path
   import time

   home = os.path.expanduser('~')
   filename = home + os.path.sep + 'src/python/examples/data/panda_color.jpg'
   filename = home + os.path.sep + 'src/python/examples/data/panda.jpg'

   src = cv2.imread(filename, cv2.IMREAD_UNCHANGED)

   startTime = time.time()
   dst = ipcv.bilateral_filter(src, 5, 50, d=-1)
   print('Elapsed time = {0} [s]'.format(time.time() - startTime))

   cv2.namedWindow(filename, cv2.WINDOW_AUTOSIZE)
   cv2.imshow(filename, src)

   cv2.namedWindow(filename + ' (Bilateral)', cv2.WINDOW_AUTOSIZE)
   cv2.imshow(filename + ' (Bilateral)', dst)

   action = ipcv.flush()
