import numpy
import cv2
import matplotlib
import matplotlib.pyplot 
import matplotlib.backends.backend_agg
def histogram(im):
   color = ('r', 'g', 'b')
   for i,col in enumerate(color):
     h = cv2.calcHist([im],[i],None,[256],[0,256])
     pdf = 
     cdf =

   return h, pdf, cdf

if __name__ == '__main__':

   import cv2
   import ipcv
   import time

   # A greyscale test image
   filename = 'crowd.jpg'
   # A 3-channel color test image
   filename = 'lenna.tif'

   im = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
   print('Data type = {0}'.format(type(im)))
   print('Image shape = {0}'.format(im.shape))
   print('Image size = {0}'.format(im.size))

   startTime = time.time()
   h, pdf, cdf = ipcv.histogram(im)
   print('Elapsed time = {0} [s]'.format(time.time() - startTime))

   axes.plot(h,color = col)
   axes.set_xlim([0,256])
   matplotlib.pyplot.show()
