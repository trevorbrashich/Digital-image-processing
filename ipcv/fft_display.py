# Author : Trevor Brashich
# Title: FFT Display


import ipcv
import cv2
import numpy as np
import sys
def fft_display(im, videoFilename=None):

   rows = im.shape[0]
   cols = im.shape[1]
   template = np.zeros((rows, cols))

   # Generates the FFt
   FFT = np.fft.fft2(im)
   FFT = np.fft.fftshift(FFT)
   logFFT = np.log10(np.abs(FFT))
   logFFT = (logFFT/np.max(logFFT)) * 255

   # Creates array to poulate with max values
   maxValues = np.flipud(np.argsort(logFFT.flatten()))
   
   used = template.copy()
   current = template.copy()
   scaled = template.copy()
   summed = template.copy()

   # creates writer and image window
   cv2.namedWindow(videoFilename)
   writer = video_writer(im.shape,videoFilename)

   for i in maxValues:
      # puts freq into used array
      used.flat[i] = logFFT.flat[i]

      # returns spatial sine wave for freq
      template.flat[i] =  logFFT.flat[i]
      current = np.fft.ifft2(template)
      template.flat[i] = 0
      
      #scales the current array and sums all freqs
      scaled = ((current - np.min(current))/ np.max(current)) *255
      summed = summed + current

      # stitching all images together
      frame =  stitch(im,logFFT,used,current,scaled,summed)
  
      if writer.isOpened():
         writer.write(frame)
      
      # shows the image
      cv2.imshow(videoFilename,frame)

      action = ipcv.flush()
      if action == "pause":
         action = ipcv.flush()
         if action == "pause":
            continue

      elif action == "exit":
         writer.release()
         sys.exit()
def video_writer(imShape, videoFilename):
   
   codec = cv2.VideoWriter_fourcc('M', 'P', 'E', 'G')
   fps = 30
   isColor = True
   videoShape = ( imShape[1],imShape[0] )
   writer = cv2.VideoWriter(videoFilename,codec,fps,videoShape,isColor)
   return writer    

def stitch(im,logFFT,used,current,scaled,summed):

   top = np.hstack( (im,logFFT,used) )
   bottom = np.hstack( (current,scaled,summed) )
   final = np.vstack( (top,bottom) ).astype(ipcv.IPCV_8U)
   return final  



if __name__ == '__main__':

   import cv2
   import ipcv
   import os.path

   home = os.path.expanduser('~')
   filename = home + os.path.sep + 'src/python/examples/data/lenna.tif'

   im = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
   if im is None:
      print('ERROR: Specified file did not contain a valid image type.')
      sys.exit(1)

   ipcv.fft_display(im)
   #   ipcv.fft_display(im, videoFilename='fft_display.mpg')

