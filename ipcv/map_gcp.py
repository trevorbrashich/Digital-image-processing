import numpy as np
import cv2
import ipcv

def map_gcp(src, map, srcX, srcY, mapX, mapY, order=1):

   nterms = (order+1)**2
   x = np.arange(nterms)
   y = [[0],[1]]

   mesh, grab = np.meshgrid(x, y)
   xExp = np.floor( mesh[0] % (order + 1) )
   yExp = np.floor(mesh[1] / (order+1))

   xMatrix = np.zeros((len(mapX), nterms))

   for indicies in range(len(mapX)):
      for term in range(nterms):
         xMatrix[indicies, term] = (mapX[indicies]**xExp[term])*(mapY[indicies]**yExp[term])      

   yMatrix = np.asmatrix([srcX, srcY]).T
   xM = np.asmatrix(xMatrix)

   X = (xMatrix.T * xM)
   C = X.I * xM.T * yMatrix

   xvals, yvals = np.meshgrid(np.arange(map.shape[0]), np.arange(map.shape[1]))

   Xp, Yp = 0, 0
   for term in range(nterms):
       Xp += C[term, 0] * (xvals**xExp[term]) * (yvals**yExp[term])
       Yp += C[term, 1] * (xvals**xExp[term]) * (yvals**yExp[term])

   Xp = Xp.astype('float32')
   Yp = Yp.astype('float32')

   return Xp, Yp


if __name__ == '__main__':

   import cv2
   import ipcv
   import os.path
   import time

   home = os.path.expanduser('~')
   imgFilename = home + os.path.sep + \
                 'src/python/examples/data/registration/image.tif'
   mapFilename = home + os.path.sep + \
                 'src/python/examples/data/registration/map.tif'
   gcpFilename = home + os.path.sep + \
                 'src/python/examples/data/registration/gcp.dat'
   src = cv2.imread(imgFilename)
   map = cv2.imread(mapFilename)

   srcX = []
   srcY = []
   mapX = []
   mapY = []
   linesRead = 0
   f = open(gcpFilename, 'r')
   for line in f:
      linesRead += 1
      if linesRead > 2:
         data = line.rstrip().split()
         srcX.append(float(data[0]))
         srcY.append(float(data[1]))
         mapX.append(float(data[2]))
         mapY.append(float(data[3]))
   f.close()

   startTime = time.clock()
   map1, map2 = ipcv.map_gcp(src, map, srcX, srcY, mapX, mapY, order=2)
   elapsedTime = time.clock() - startTime
   print('Elapsed time (map creation) = {0} [s]'.format(elapsedTime)) 

   startTime = time.clock()
   dst = cv2.remap(src, map1, map2, cv2.INTER_NEAREST)
 #   dst = ipcv.remap(src, map1, map2, ipcv.INTER_NEAREST)
   elapsedTime = time.clock() - startTime
   print('Elapsed time (remap) = {0} [s]'.format(elapsedTime)) 

   srcName = 'Source (' + imgFilename + ')'
   cv2.namedWindow(srcName, cv2.WINDOW_AUTOSIZE)
   cv2.imshow(srcName, src)

   mapName = 'Map (' + mapFilename + ')'
   cv2.namedWindow(mapName, cv2.WINDOW_AUTOSIZE)
   cv2.imshow(mapName, map)

   dstName = 'Warped (' + mapFilename + ')'
   cv2.namedWindow(dstName, cv2.WINDOW_AUTOSIZE)
   cv2.imshow(dstName, dst)

   ipcv.flush()

