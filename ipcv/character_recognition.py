





import numpy as np
import ipcv
import cv2
def character_recognition(src,
                          templates,
                          codes,
                          threshold,
                          filterType='spatial'):
   # for every template given it builds a 2d map where template matches character
   results = []
   text = []
   mapText = {}
   if (filterType == 'spatial'):
       
      for character in templates:
         #uses cv2 filter to find points
         matched = cv2.filter2D(src, -1, character)

         # makes single points using np.where and turns into array
         matchPoint = np.where(matched >= threshold, 0, 255)
         matchPoint = np.array(matchPoint, matched.dtype)
         
         #appends results to list
         results.append((matchPoint/255).sum())

         coordinates = np.where(matchPoint >= threshold)
         for coordIndices in range(len(coordinates[0])):
            coords = (coordinates[0][coordIndices], coordinates[1][coordIndices])    
            

   return results, text



if __name__ == '__main__':
   import numpy as np
   import matplotlib.pyplot
   import cv2
   import fnmatch
   import numpy
   import os
   import os.path

   home = os.path.expanduser('~')
   baseDirectory = home + os.path.sep + 'src/python/examples/data'
   baseDirectory += os.path.sep + 'character_recognition'

   documentFilename = baseDirectory + '/notAntiAliased/text.tif'
   documentFilename = baseDirectory + '/notAntiAliased/alphabet.tif'
   charactersDirectory = baseDirectory + '/notAntiAliased/characters'

   document = cv2.imread(documentFilename, cv2.IMREAD_UNCHANGED)

   characterImages = []
   characterCodes = []
   for root, dirnames, filenames in os.walk(charactersDirectory):
      for filename in sorted(filenames):
         currentCharacter = cv2.imread(root + os.path.sep + filename,
                                       cv2.IMREAD_UNCHANGED)
         characterImages.append(currentCharacter)
         code = int(os.path.splitext(os.path.basename(filename))[0])
         characterCodes.append(code)
   characterImages = numpy.asarray(characterImages)
   characterCodes = numpy.asarray(characterCodes)

   # Define the filter threshold
   threshold = 1.0

   text, histogram = character_recognition(document, 
                                           characterImages, 
                                           characterCodes, 
                                           threshold, 
                                           filterType='spatial')

   # Display the results to the user
   for n in range(len(characterCodes)):
      print(str(characterCodes[n]) + ": "+ str(histogram[n]))

   characterNames = np.array(characterCodes)
   pos = np.arange(len(characterNames))
   width = 1.0     # gives histogram aspect to the bar diagram

   matplotlib.pyplot.figure(1)
   matplotlib.pyplot.subplot(3, 1, 1)
   matplotlib.pyplot.xticks(pos + (width / 2))
   matplot.lib.pyplot.xlabels(characterNames)
#
   matplotlib.pyplot.bar(pos, histogram, width, color='r')
   matplotlib.pyplot.show()

   text = []
   for i in text:
      text.append(characterCodes[i])

   print("Text:\n", text)
         

  # text, histogram = character_recognition(document, 
  #                                         characterImages, 
  #                                         characterCodes, 
  #                                         threshold, 
  #                                         filterType='matched')

   # Display the results to the user
        # .
        # .
        # .

