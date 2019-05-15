import numpy as np
import numerical

def idft(F, scale=False):

   def swap(F):
      return F.real*(0+1j) + F.imag    

   M = F.shape[0]
   scaleFactor = 1
   if (scale):
      scaleFactor = (1/M)

   ift = swap(numerical.dft(swap(F)))/scaleFactor

   return ift

    
if __name__ == '__main__':
   import numerical
   import numpy
   import time

   N = 2**12
   F = numpy.zeros(N, dtype=numpy.complex128)
   F[0] = 1

   repeats = 10
   print('Repetitions = {0}'.format(repeats))

   startTime = time.clock()
   for repeat in range(repeats):
      f = numerical.idft(F)
   string = 'Average time per transform = {0:.8f} [s] ({1}-point iDFT)'
   print(string.format((time.clock() - startTime)/repeats, len(F)))

   startTime = time.clock()
   for repeat in range(repeats):
      f = numpy.fft.ifft(F)
   string = 'Average time per transform = {0:.8f} [s] ({1}-point iFFT)'
   print(string.format((time.clock() - startTime)/repeats, len(F)))


