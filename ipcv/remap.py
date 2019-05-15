import cv2
import ipcv
import numpy as np

def remap(src, map1, map2, interpolation=ipcv.INTER_NEAREST, borderMode=ipcv.BORDER_CONSTANT, borderValue=0):

   if len(src.shape) == 3:
      dst = np.zeros((map1.shape[0], map1.shape[1], src.shape[2]))
   else:
      dst = np.zeros((map1.shape[0], map1.shape[1], 1))   

   if (borderMode==ipcv.BORDER_CONSTANT):
      dst.fill(borderValue)    
   else:
      raise ValueError('borderMode not supported')

   if (interpolation == ipcv.INTER_NEAREST):
      m1 = np.ma.masked_outside(map1, 0, src.shape[0])
      m1 = np.around(m1)
      m1 = np.ma.array(m1, dtype=src.dtype)

      
      m2 = np.ma.masked_outside(map2, 0, src.shape[1])
      m2 = np.around(m2)
      m2 = np.ma.array(m2, dtype=src.dtype)
   
   else:
      raise ValueError('Interpolation not supported, use Nearest Neighbor')


   dst = src[m1, m2, :]
   return dst

if __name__ == '__main__':

   import cv2
   import ipcv
   import os.path
   import time

   home = os.path.expanduser('~')
   filename = home + os.path.sep + 'src/python/examples/data/crowd.jpg'
   filename = home + os.path.sep + 'src/python/examples/data/lenna.tif'
   src = cv2.imread(filename)

   map1, map2 = ipcv.map_rotation_scale(src, rotation=30, scale=[1.3, 0.8])

   startTime = time.clock()
   dst = ipcv.remap(src, map1, map2, interpolation=ipcv.INTER_NEAREST, borderMode=ipcv.BORDER_CONSTANT, borderValue=0)
   elapsedTime = time.clock() - startTime
   print('Elapsed time (remap) = {0} [s]'.format(elapsedTime))

   srcName = 'Source (' + filename + ')'
   cv2.namedWindow(srcName, cv2.WINDOW_AUTOSIZE)
   cv2.imshow(srcName, src)

   dstName = 'Destination (' + filename + ')'
   cv2.namedWindow(dstName, cv2.WINDOW_AUTOSIZE)
   cv2.imshow(dstName, dst)

   ipcv.flush()
