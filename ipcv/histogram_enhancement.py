"""
   title:: 
      histogram_enhancement.py

   description::
      this program reads in an image that is given and searches for the amount of
      channels it has. based on the channels the program runs either gray-scale or color
      enhancement and histogram matching. 
   attributes::
      image - image being enhanced
      etype - the type of enhancement being performed
      target - the target image to match against the original image
      maxCount - the max DC value of the image
   returns::
      enhanced image, in this case the output image that has been enhanced 
   author::
      Trevor Brashich
"""

import cv2
import numpy as np
import ipcv
import numpy

def cdf_build(array, dcVals):
   #if single channel the pdf = array or im being called 
   if (len(np.shape(array)) == 1):
      pdf = array
  
  # checks amount of channels, gets histogram from the image 
   else:
      if (len(np.shape(array)) == 2):
         hist = cv2.calcHist([array],[0], None, [dcVals], [0, dcVals])
  
      elif (len(np.shape(im)) == 3):
         hist = cv2.calcHist([im], [0], None, [dcVals], [0, dcVals])
      
      # pdf is equal to probability of histogram value / total pixels in image
      pdf = hist / np.prod(np.shape((array)))

   #cdf is cumulative sum of the probabilities or pdf
   cdf = np.cumsum(pdf)
   return cdf

def build_match_lut(im ,target, maxCount):
   imageCDF = cdf_build(im, maxCount)
   targetCDF = cdf_build(target, maxCount)
   # creates cdf based off image and target image

   # builds the look up table
   lut = np.arange(maxCount + 1)

   for i in range(maxCount):
      
      # sets the imagecdf max to maxCount of target
      if (imageCDF[i] > np.amax(targetCDF)):
         lut[i] = maxCount
      
      else:
      
         lut[i] = np.argmax(np.where(targetCDF >= imageCDF[i], 1, 0))    
   
   return lut      


def build_lut(im, value, dcVals):
#builds linear look up table for given image

   cdf = cdf_build(im, dcVals - 1)
   
   # removes value/2 from each side of cdf
   # gets lower and upper end of the cdf
   lowerCDF = cdf - ((value / 2) / 100)
   upperCDF = (-cdf + 1) - ((value / 2) / 100)

   absLowCDF = np.absolute(lowerCDF)
   absUpCDF = np.absolute(upperCDF)

   minIndex = np.argmin(absLowCDF)
   maxIndex = np.argmin(absUpCDF)

   # finds the slope and intercept over the values that will be changed
   slope = dcVals / (maxIndex - minIndex)
   intercept = (slope * minIndex)
 
   # creates a linear array based of pixel values
   linArray = np.arange(dcVals)

   # clips the array to 0 from minIndex and maxes out from maxIndex
   lowClip = linArray < minIndex
   upperClip = linArray > maxIndex

   linArray = (slope * linArray) - intercept

   np.place(linArray, lowClip, 0)
   np.place(linArray, upperClip, dcVals - 1)

   return linArray

def build_color_lut(im, value, dcVals):
# builds a linear color look up table
    
   #creates a look up table for each color channel 
   rlut = build_lut(im[:, :, 2], value, dcVals)
   glut = build_lut(im[:, :, 1], value, dcVals)
   blut = build_lut(im[:, :, 0], value, dcVals)

   return np.array([blut, glut, rlut])

def build_match_color_lut(im, target, maxCount):
# bulds a color look up table for a given color image (target image)

   #checks amount of channels to see if image is color or grayscale
   if (len(np.shape(target)) == 3): 
      rlut = build_match_lut(im[:, :, 2], target[:, :, 2], maxCount)
      glut = build_match_lut(im[:, :, 1], target[:, :, 1], maxCount)
      blut = build_match_lut(im[:, :, 0], target[:, :, 0], maxCount)

   else:

      rlut = build_match_lut(im[:, :, 2], target, maxCount)
      glut = build_match_lut(im[:, :, 1], target, maxCount)
      blut = build_match_lut(im[:, :, 0], target, maxCount)        

   return np.array([blut, glut, rlut])

def histogram_enhancement(im, etype='linear2', target=None, maxCount=255):
 
   outputIm = np.zeros((im.shape))
 
   # error checking
   if (not isinstance(im, np.ndarray)):
      raise TypeError('image is not an numpy ndarray')

   if (not isinstance(etype, str)):
      raise TypeError('etype must be a string')    

   # performs linear enhancement based of linear percentage
   if (etype.find('linear') == 0):
      linVal = etype.split("linear")[1] 


      if (not linVal.isdigit()):
         raise RuntimeError('etype should contain a digit') 
  
      # linVal is the digit found in the linear string, percentage to enhance by
      linPercentage = int(linVal)

      #checks if image is color
      if (len(np.shape(im)) == 3):
      
         lut = build_color_lut(im, linPercentage, maxCount + 1)    
         outputIm[:, :, 0] = lut[0][im[:, :, 0]]
         outputIm[:, :, 1] = lut[1][im[:, :, 1]]
         outputIm[:, :, 2] = lut[2][im[:, :, 2]]

      else:
     
         lut = build_lut(im, linPercentage, maxCount + 1)
         outputIm = lut[im]

   elif etype == 'match':
      if (not isinstance(target, np.ndarray)):
         raise TypeError('target is not a numpy ndarray')
      else:
         #checks if image is color and performs match enhancement
         if (len(np.shape(im)) == 3):     
            lut = build_match_color_lut(im, target, maxCount)
            outputIm[:,:,0] = lut[0][im[:,:,0]]
            outputIm[:,:,1] = lut[1][im[:,:,1]]
            outputIm[:,:,2] = lut[2][im[:,:,2]]
        
         # if not a color image performs grayscale matching enhancement
         else:
            lut = build_match_lut(im, target, maxCount)
            outputIm = lut[im]

   elif (etype == 'equalize'):
      #build a pdf to match the image against 
      equalizePDF = np.zeros(maxCount)
      equalizePDF.fill(1/maxCount)

      if (len(np.shape(im)) == 3):
         #performs color match enhancement
         lut = build_match_color_lut(im, equalizePDF, maxCount)
         outputIm[:,:,0] = lut[0][im[:,:,0]]
         outputIm[:,:,1] = lut[1][im[:,:,1]]
         outputIm[:,:,2] = lut[2][im[:,:,2]]
      
      else:
         lut = build_match_lut(im, equalizePDF, maxCount)
         outputIm = lut[im]

   else:
      raise ValueError("etype must be 'linear', 'match' or 'equalize'")
      # raises error if none of the etypes match 
  
   outputIm = np.array(outputIm, im.dtype)  
   return outputIm


if __name__ == '__main__':

   import cv2
   import ipcv
   import os.path
   import time

   home = os.path.expanduser('~')
   #filename = home + os.path.sep + 'src/python/examples/data/redhat.ppm'
   #filename = home + os.path.sep + 'src/python/examples/data/crowd.jpg'
   #filename = home + os.path.sep + 'src/python/examples/data/lenna.tif'
   filename = home + os.path.sep + 'src/python/examples/data/giza.jpg'

   matchFilename = home + os.path.sep + 'src/python/examples/data/giza.jpg'
   #matchFilename = home + os.path.sep + 'src/python/examples/data/lenna.tif'
   #matchFilename = home + os.path.sep + 'src/python/examples/data/redhat.ppm'
   #matchFilename = home + os.path.sep + 'src/python/examples/data/crowd.jpg'

   im = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
   print('Filename = {0}'.format(filename))
   print('Data type = {0}'.format(type(im)))
   print('Image shape = {0}'.format(im.shape))
   print('Image size = {0}'.format(im.size))

   cv2.namedWindow(filename, cv2.WINDOW_AUTOSIZE)
   cv2.imshow(filename, im)

   print('Linear 2% ...')
   startTime = time.time()
   enhancedImage = ipcv.histogram_enhancement(im, etype='linear2')
   print('Elapsed time = {0} [s]'.format(time.time() - startTime))
   cv2.namedWindow(filename + ' (Linear 2%)', cv2.WINDOW_AUTOSIZE)
   cv2.imshow(filename + ' (Linear 2%)', enhancedImage)

   print('Linear 1% ...')
   startTime = time.time()
   enhancedImage = ipcv.histogram_enhancement(im, etype='linear1')
   print('Elapsed time = {0} [s]'.format(time.time() - startTime))
   cv2.namedWindow(filename + ' (Linear 1%)', cv2.WINDOW_AUTOSIZE)
   cv2.imshow(filename + ' (Linear 1%)', enhancedImage)

   print('Equalized ...')
   startTime = time.time()
   enhancedImage = ipcv.histogram_enhancement(im, etype='equalize')
   print('Elapsed time = {0} [s]'.format(time.time() - startTime))
   cv2.namedWindow(filename + ' (Equalized)', cv2.WINDOW_AUTOSIZE)
   cv2.imshow(filename + ' (Equalized)', enhancedImage)

   tgtIm = cv2.imread(matchFilename, cv2.IMREAD_UNCHANGED)
   print('Matched (Image) ...')
   startTime = time.time()
   enhancedImage = ipcv.histogram_enhancement(im, etype='match', target=tgtIm)
   print('Elapsed time = {0} [s]'.format(time.time() - startTime))
   cv2.namedWindow(filename + ' (Matched - Image)', cv2.WINDOW_AUTOSIZE)
   cv2.imshow(filename + ' (Matched - Image)', enhancedImage)

   tgtPDF = numpy.ones(256) / 256
   print('Matched (Distribution) ...')
   startTime = time.time()
   enhancedImage = ipcv.histogram_enhancement(im, etype='match', target=tgtPDF)
   print('Elapsed time = {0} [s]'.format(time.time() - startTime))
   cv2.namedWindow(filename + ' (Matched - Distribution)', cv2.WINDOW_AUTOSIZE)
   cv2.imshow(filename + ' (Matched - Distribution)', enhancedImage)

   action = ipcv.flush()

