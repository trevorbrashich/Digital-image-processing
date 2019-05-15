import cv2
import time
import numpy
import matplotlib.pyplot
import matplotlib

def histogram(im):
   """
   title:: 
      histogram(opencv method)

   description::
     this method uses the opencv library to calculate a histogram
     each histogram, r/g/b is calculated using different channels.
     the method also create a PDF and CDF based of the histogram
   attributes::
     image: the image used, can be color rgb or grayscale
   returns::
     the method returns the histogram, the probability 
     density function and the cumulative density function
 
   author::
      Trevor Brashich
   """

  # hist = cv2.calcHist([im], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
  # histo = hist.flatten()
  # h = histo 
   
   redhist = cv2.calcHist([im], [2], None, [256], [0,256])
   greenhist = cv2.calcHist([im], [0], None, [256], [0,256])
   bluehist = cv2.calcHist([im], [1], None, [256], [0,256])

   h = [redhist, bluehist, greenhist]
   [r, c, b] = im.shape
#   print(r, c, b)
   pdfblue =[]
   pdfgreen = []
   pdfred = []
   for i in range(len(bluehist)):
        pdfblue.append(bluehist[i]/float((r*c)))

   for i in range(len(greenhist)):
        pdfgreen.append(greenhist[i]/float((r*c)))  

   for i in range(len(redhist)):
        pdfred.append(redhist[i]/float((r*c)))

   pdf = [pdfred, pdfblue, pdfgreen]
   
   cdfRed = numpy.cumsum(pdf[0])
   cdfGreen = numpy.cumsum(pdf[1])
   cdfBlue = numpy.cumsum(pdf[2])
#   sumB = 0
#   sumG = 0
#   sumR = 0
#   cdfBlue = []
#   cdfGreen = []
#   cdfRed = []
#   for i in range(len(pdfblue)):
#     sumB += pdfblue[i]
#     cdfBlue.append(sumB)

#   for i in range(len(pdfgreen)):
#     sumG += pdfgreen[i]
#     cdfGreen.append(sumG)

#   for i in range(len(pdfred)):
#      sumR += pdfred[i]
#      cdfRed.append(sumR)
        
   cdf = [cdfRed, cdfGreen, cdfBlue]

   return h, pdf, cdf



if __name__ == '__main__':

   import cv2
   import ipcv
   import time

   # A greyscale test image
   #filename = 'crowd.jpg'
   # A 3-channel color test image
   filename = 'lenna.tiff'

   im = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
   print('Data type = {0}'.format(type(im)))
   print('Image shape = {0}'.format(im.shape))
   print('Image size = {0}'.format(im.size))

   startTime = time.time()
   h, pdf, cdf = ipcv.histogram(im)
   print('Elapsed time = {0} [s]'.format(time.time() - startTime))

   Max = range(256)

   if len(im.shape) == 3:
        [histR, histG, histB] = h
        [pdfR, pdfG, pdfB] = pdf
        [cdfR, cdfG, cdfB] = cdf

        matplotlib.pyplot.figure(1)

        matplotlib.pyplot.subplot(3, 1, 1)
        matplotlib.pyplot.ylabel('number of pixels')
        matplotlib.pyplot.xlabel('Digital Count')
        matplotlib.pyplot.xlim([0,256])
        matplotlib.pyplot.plot(Max, histR, 'r-')
        matplotlib.pyplot.plot(Max, histG, 'g-')
        matplotlib.pyplot.plot(Max, histB, 'b-')

        matplotlib.pyplot.subplot(3, 1, 2)
        matplotlib.pyplot.ylabel('pdf')
        matplotlib.pyplot.xlabel('Digital Count')
        matplotlib.pyplot.xlim([0,256])
        matplotlib.pyplot.plot(Max, pdfR, 'r-')
        matplotlib.pyplot.plot(Max, pdfG, 'g-')
        matplotlib.pyplot.plot(Max, pdfB, 'b-')

        matplotlib.pyplot.subplot(3, 1, 3)
        matplotlib.pyplot.ylabel('cdf')
        matplotlib.pyplot.xlabel('Digital Count')
        matplotlib.pyplot.xlim([0,256])
        matplotlib.pyplot.plot(Max, cdfR, 'r-')
        matplotlib.pyplot.plot(Max, cdfG, 'g-')
        matplotlib.pyplot.plot(Max, cdfB, 'b-')

        matplotlib.pyplot.show()

   if len(im.shape) == 2:
        [histRows, histCols] = h
        [pdfRows, pdfCols] = pdf
        [cdfRows, cdfCols] = cdf

        matplotlib.pyplot.figure(1)
        matplotlib.pyplot.subplot(3, 1, 1)
        matplotlib.pyplot.plot(Max, h, 'k-')

        matplotlib.pyplot.subplot(3, 1, 2)
        matplotlib.pyplot.plot(Max, pdf, 'k-')

        matplotlib.pyplot.subplot(3, 1, 3)
        matplotlib.pyplot.plot(Max, cdf, 'k-')

        matplotlib.pyplot.show()




