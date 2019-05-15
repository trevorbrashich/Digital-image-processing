import ipcv
import cv2
import numpy as np

def map_quad_to_quad(img, map, imgX, imgY, mapX, mapY):
   
   transformationMatrix = np.matrix([[mapX[0], mapY[0], 1, 0, 0, 0, -mapX[0]*imgX[0], -mapY[0]*imgX[0]],
                                     [mapX[1], mapY[1], 1, 0, 0, 0, -mapX[1]*imgX[1], -mapY[1]*imgX[1]],
                                     [mapX[2], mapY[2], 1, 0, 0, 0, -mapX[2]*imgX[2], -mapY[2]*imgX[2]],
                                     [mapX[3], mapY[3], 1, 0, 0, 0, -mapX[3]*imgX[3], -mapY[3]*imgX[3]],
                                     [0, 0, 0, mapX[0], mapY[0], 1, -mapX[0]*imgY[0], -mapY[0]*imgY[0]],
                                     [0, 0, 0, mapX[1], mapY[1], 1, -mapX[1]*imgY[1], -mapY[1]*imgY[1]],
                                     [0, 0, 0, mapX[2], mapY[2], 1, -mapX[2]*imgY[2], -mapY[2]*imgY[2]],
                                     [0, 0, 0, mapX[3], mapY[3], 1, -mapX[3]*imgY[3], -mapY[3]*imgY[3]]])
                                    
   tMatrix = np.asmatrix(transformationMatrix).I
   xM = np.matrix([imgX[0], imgX[1], imgX[2], imgX[3], imgY[0], imgY[1], imgY[2], imgY[3]])
   xMatrix = xM.reshape(8, 1)
   
   pM = (tMatrix * xMatrix)
   P = np.insert(pM, 8, [1])
   pMatrix = P.reshape(3, 3) 
   print (pMatrix)

   I = np.indices((map.shape[1], map.shape[0]))
   i0 = I[0].flatten()
   i1 =  I[1].flatten()
   ones = np.ones(i1.size)       
   
   iM = np.matrix([i1, i0, ones])
   product = (pMatrix * iM)
   p = np.array(product)
   xvals = p[0] / p[2]
   yvals = p[1] / p[2]
 
   print (iM)
   print (map.shape)
   x = xvals.reshape(map.shape[1], map.shape[0])
   y = yvals.reshape(map.shape[1], map.shape[0])
  
   x = x.astype(np.float32)
   y = y.astype(np.float32)
   

   return x, y
if __name__ == '__main__':

   import cv2
   import ipcv
   import os.path
   import time
   import numpy

   home = os.path.expanduser('~')
   imgFilename = home + os.path.sep + 'src/python/examples/data/lenna.tif'
   mapFilename = home + os.path.sep + 'src/python/examples/data/gecko.jpg'
   img = cv2.imread(imgFilename)
   map = cv2.imread(mapFilename)

   mapName = 'Select corners for the target area (CW)'
   cv2.namedWindow(mapName, cv2.WINDOW_AUTOSIZE)
   cv2.imshow(mapName, map)

   print('')
   print('--------------------------------------------------------------')
   print('  Select the corners for the target area of the source image')
   print('  in clockwise order beginning in the upper left hand corner')
   print('--------------------------------------------------------------')
   p = ipcv.PointsSelected(mapName, verbose=True)
   while p.number() < 4:
      cv2.waitKey(100)
   cv2.destroyWindow(mapName)

   imgX = [0, img.shape[1]-1, img.shape[1]-1, 0]
   imgY = [0, 0, img.shape[0]-1, img.shape[0]-1]
   mapX = p.x()
   mapY = p.y()

   print('')
   print('Image coordinates ...')
   print('   x -> {0}'.format(imgX))
   print('   y -> {0}'.format(imgY))
   print('Target (map) coordinates ...')
   print('   u -> {0}'.format(mapX))
   print('   v -> {0}'.format(mapY))
   print('')

   startTime = time.clock()
   map1, map2 = ipcv.map_quad_to_quad(img, map, imgX, imgY, mapX, mapY)
   elapsedTime = time.clock() - startTime
   print('Elapsed time (map creation) = {0} [s]'.format(elapsedTime)) 

   startTime = time.clock()
   dst = cv2.remap(img, map1, map2, cv2.INTER_NEAREST)
   elapsedTime = time.clock() - startTime
   print('Elapsed time (remap) = {0} [s]'.format(elapsedTime)) 
   print('')

   compositedImage = map
   mask = numpy.where(dst != 0)
   if len(mask) > 0:
      compositedImage[mask] = dst[mask]

   compositedName = 'Composited Image'
   cv2.namedWindow(compositedName, cv2.WINDOW_AUTOSIZE)
   cv2.imshow(compositedName, compositedImage)

   ipcv.flush()
