import numpy as np
import numerical

def dft(f, scale=True):

   M = f.shape[0]
   u = np.arange(M)

   rotatedU = u.reshape(u.shape[0],1)

   theta = (2 * np.pi * u * rotatedU) / M
   e = np.cos(theta) - (np.sin(theta) * (0+1j))
 
   scaleFactor = 1
   if (scale):
      scaleFactor = (1/M)

   ft = scaleFactor * np.sum((f*e), axis = 1)
   return ft


if __name__ == '__main__':

   import numerical
   import numpy
   import time

   N = 2**12
   f = numpy.ones(N, dtype=numpy.complex128)

   repeats = 10
   print('Repetitions = {0}'.format(repeats))

   startTime = time.clock()
   for repeat in range(repeats):
      F = numerical.dft(f)
   string = 'Average time per transform = {0:.8f} [s] ({1}-point DFT)'
   print(string.format((time.clock() - startTime)/repeats, len(f)))

   startTime = time.clock()
   for repeat in range(repeats):
      F = numpy.fft.fft(f)
   string = 'Average time per transform = {0:.8f} [s] ({1}-point FFT)'
   print(string.format((time.clock() - startTime)/repeats, len(f)))

