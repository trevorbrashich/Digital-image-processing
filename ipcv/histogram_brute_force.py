import ipcv
import cv2
import time
import numpy
import matplotlib.pyplot
import matplotlib

def histogram(im):
    """
    title:: 
      histogram(brute force)

    description::
     this method uses only python to generate histograms for each channel.
     each histogram, r/g/b is calculated by finding the amount of
     r,g,b pixel values. The method also create a PDF and CDF based of the histogram
    attributes::
     image: the image used, can be color rgb or grayscale
    returns::
     the method returns the histogram, the probability 
     density function and the cumulative density function
 
    author::
      Trevor Brashich
    """

    try:
        [rows, cols, bands] = image.shape
    except:
        bands = 1   

    redHist = [0] *256
    greenHist = [0] *256
    blueHist = [0] *256
    [r,c,b] = im.shape
    for rows in range(r):

        for cols in range(c):

            for bands in range(b):
                if bands ==0:
                    blueHist[im[rows,cols,bands]] +=1
                if bands == 1:
                    greenHist[im[rows,cols,bands]] +=1
                if bands == 2:
                    redHist[im[rows,cols,bands]] +=1

    h = [redHist, greenHist, blueHist]
    pdfBlue =[]
    pdfGreen = []
    pdfRed = []
    for i in range(len(blueHist)):
        pdfBlue.append(blueHist[i]/float((r*c)))

    for i in range(len(greenHist)):
        pdfGreen.append(greenHist[i]/float((r*c)))  

    for i in range(len(redHist)):
        pdfRed.append(redHist[i]/float((r*c)))

    pdf = [pdfRed, pdfGreen, pdfBlue]

    sumB = 0
    sumG = 0
    sumR = 0
    cdfBlue = []
    cdfGreen = []
    cdfRed = []
    for i in range(len(pdfBlue)):
        sumB += pdfBlue[i]
        cdfBlue.append(sumB)

    for i in range(len(pdfGreen)):
        sumG += pdfGreen[i]
        cdfGreen.append(sumG)

    for i in range(len(pdfRed)):
        sumR += pdfRed[i]
        cdfRed.append(sumR)
        
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
        matplotlib.pyplot.plot(Max, histR, 'r-')
        matplotlib.pyplot.plot(Max, histG, 'g-')
        matplotlib.pyplot.plot(Max, histB, 'b-')

        matplotlib.pyplot.subplot(3, 1, 2)
        matplotlib.pyplot.ylabel('pdf')
        matplotlib.pyplot.xlabel('Digital Count')
        matplotlib.pyplot.plot(Max, pdfR, 'r-')
        matplotlib.pyplot.plot(Max, pdfG, 'g-')
        matplotlib.pyplot.plot(Max, pdfB, 'b-')

        matplotlib.pyplot.subplot(3, 1, 3)
        matplotlib.pyplot.ylabel('cdf')
        matplotlib.pyplot.xlabel('Digital Count')        
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




















































































































































