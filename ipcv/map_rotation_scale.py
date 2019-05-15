import numpy as np
import ipcv
import cv2
def map_rotation_scale(src, rotation=0, scale=[1, 1]):

   degree = np.radians(rotation)

   rMatrix = np.array([
       np.cos(degree),
       np.sin(degree),
       -np.sin(degree),
       np.cos(degree)
   ])
   
   rMatrix = rMatrix.reshape(2,2)

   sMatrix = np.array([scale[0], 0, 0, scale[1]])    

   sMatrix = sMatrix.reshape(2,2)

   tMatrix = np.dot(rMatrix, sMatrix)


   mapCorners = np.array([
        [-src.shape[0]/2, src.shape[1]/2],
        [src.shape[0]/2, src.shape[1]/2],
        [-src.shape[0]/2, -src.shape[1]/2],
        [src.shape[0]/2, -src.shape[1]/2]
   ])

   minX, minY = float('inf'), float('inf')
   maxX, maxY = float('-inf'), float('-inf')

   for xyPair in mapCorners:
      x, y = np.dot(tMatrix, xyPair)
      minX = min(minX, x)
      minY = min(minY, y)
      maxX = max(maxX, x)
      maxY = max(maxY, y)

   widthX = maxX - minX
   widthY =  maxY - minY

   wX = widthX.astype(np.int64)
   wY = widthY.astype(np.int64)
   xvals = np.zeros((wY, wX))
   yvals = np.zeros((wY, wX))

   for row in range(xvals.shape[0]):
      for column in range(xvals.shape[1]):
         offsetX = column - (xvals.shape[1] / 2)
         offsetY = (xvals.shape[0] / 2) - row

         offset = np.array([offsetX, offsetY])

         transMatrix = np.asmatrix(tMatrix).I
         offset = np.asmatrix(offset.reshape(2,1))
         xp, yp = transMatrix*offset

         
         unoffsetX = (xp + (src.shape[1]/2))
         unoffsetY = ((src.shape[0]/2) - yp)

         xvals[row,column] = unoffsetX
         yvals[row,column] = unoffsetY

   xvals = xvals.astype('float32')
   yvals = yvals.astype('float32')
   return (xvals, yvals)

if __name__ == '__main__':

   import cv2
   import ipcv
   import os.path
   import time

   home = os.path.expanduser('~')
   filename = home + os.path.sep + 'src/python/examples/data/crowd.jpg'
   filename = home + os.path.sep + 'src/python/examples/data/lenna.tif'
   src = cv2.imread(filename)

   startTime = time.clock()
   map1, map2 = ipcv.map_rotation_scale(src, rotation=30, scale=[1.3, 0.8])
   elapsedTime = time.clock() - startTime
   print('Elapsed time (map creation) = {0} [s]'.format(elapsedTime))

   startTime = time.clock()
   dst = cv2.remap(src, map1, map2, cv2.INTER_NEAREST, borderMode = ipcv.BORDER_REPLICATE)
   #dst = ipcv.remap(src, map1, map2, ipcv.INTER_NEAREST)
   elapsedTime = time.clock() - startTime
   print('Elapsed time (remapping) = {0} [s]'.format(elapsedTime)) 

   srcName = 'Source (' + filename + ')'
   cv2.namedWindow(srcName, cv2.WINDOW_AUTOSIZE)
   cv2.imshow(srcName, src)

   dstName = 'Destination (' + filename + ')'
   cv2.namedWindow(dstName, cv2.WINDOW_AUTOSIZE)
   cv2.imshow(dstName, dst)

   ipcv.flush()


