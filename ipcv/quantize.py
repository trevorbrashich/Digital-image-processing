"""
   title:: 
      quantize.py

   description::
      this method uses image quantization to decrease the amount of bits within the new
      image therefore creating a smaller file. Uniform quantization scales the dc within each bin 
      to the lowest integer of the maxCount + 1 divided by the levels. The IGS quantization adds on
      the remainder to the next new digital count
   attributes::
      image - the image being referenced, can be any number of channels
      levels - integer value 
      qtype - the type of quantization being performed
      maxCount - the alloted amount of digital count
      displayLevels - the range of the digital count values alloted for the image quantization
   returns::
      quantizedImage, Image, both uniform and IGS quantized image 
   author::
      Trevor Brashich
"""


import cv2
import ipcv
import math
import numpy as np
def quantize(im, levels, qtype='uniform', maxCount=255, displayLevels=None):
   # checks displayLevels to make sure it matches, if not it re-expands
   if displayLevels == None: 
     scale = 1
   else:
     scale = displayLevels // levels
   
   #finds the DC width of each level
   binsize = ((maxCount+1)/levels)
   print(binsize)

   # Uniform quantization method
   if qtype == 'uniform':
     # performs integer division of the numpynd array and the binsize 
     DCquantize = (im//binsize)
     DCquantized = DCquantize * (displayLevels/levels)
     # makes sure the data type is correct
     quantizedImage = DCquantized.astype(im.dtype)
     return quantizedImage      
   
   elif qtype == 'igs':         
     # sets error to zero
     error = 0
     #creates empty list of return values
     ReturnList = []
     quantizedIm = np.reshape(im, im.size)
     divider = (maxCount + 1) / float(levels)
     for i in range(len(im)):
         RowList = []
         for j in range(len(im)):  
           # adds error to new DC
           quantizedIm = im[i][j] + error
           # clips values to maxCount
           if quantizedIm > maxCount:
               quantizedIm = maxCount
           error = quantizedIm % (divider)
           DC = (quantizedIm) // divider
           # appends the new digital count to the row
           RowList.append(DC*(displayLevels//levels))
         # appends the row to return list for final image
         ReturnList.append(np.array(RowList))
     quantizedImage = np.array(ReturnList,im.dtype)    
     return quantizedImage

   # checks qtype to see if invalid
   elif qtype != 'uniform' or qtype != 'igs':
     raise RuntimeError('qtype is not supported')
     print('quantizing image uniformly')
     # quantizes uniformly by default if invalid
     quantizedImage = numpy.floor(im / divider)
     return quantizedImage
if __name__ == '__main__':

   import cv2
   import ipcv
   import os.path

   home = os.path.expanduser('~')
  # filename = home + os.path.sep + 'src/python/examples/data/crowd.jpg'
  # filename = home + os.path.sep + 'src/python/examples/data/redhat.ppm'
   filename = home + os.path.sep + 'src/python/examples/data/linear.tif'
  # filename = home + os.path.sep + 'src/python/examples/data/lenna.tif'

   im = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
   print('Filename = {0}'.format(filename))
   print('Data type = {0}'.format(type(im)))
   print('Image shape = {0}'.format(im.shape))
   print('Image size = {0}'.format(im.size))

   cv2.namedWindow(filename, cv2.WINDOW_AUTOSIZE)
   cv2.imshow(filename, im)

   numberLevels = 7
   quantizedImage = ipcv.quantize(im,
                                  numberLevels,
                                  qtype='uniform',
                                  displayLevels=256)
   cv2.namedWindow(filename + ' (Uniform Quantization)', cv2.WINDOW_AUTOSIZE)
   cv2.imshow(filename + ' (Uniform Quantization)', quantizedImage)
   
   numberLevels = 7
   quantizedImage = ipcv.quantize(im,
                                  numberLevels,
                                  qtype='igs',
                                  displayLevels=256)
   cv2.namedWindow(filename + ' (IGS Quantization)', cv2.WINDOW_AUTOSIZE)
   cv2.imshow(filename + ' (IGS Quantization)', quantizedImage)
   
   action = ipcv.flush()
   
