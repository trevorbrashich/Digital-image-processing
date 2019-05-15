import numpy as np
import numerical
def dft2(f, scale=True):

   c = f.swapaxes(0,1)
   Columns = []
   for col in range(c.shape[0]):
      Columns.append(numerical.dft(c[col], False))

   x = np.array(Columns)
   r = x.swapaxes(0,1)
   Rows = []

   
   for row in range(r.shape[0]):
      Rows.append(numerical.dft(r[row], False))
   
   fU = np.array(Rows)

   M = f.shape[0]*f.shape[1]
   scaleFactor = 1
   if (scale):
      scaleFactor = (1/M)

   return fU*scaleFactor


if __name__ == '__main__':
    import numerical
    import numpy
    import time

    M = 2**5
    N = 2**5
    f = numpy.ones((M,N), dtype=numpy.complex128)

    repeats = 10
    print('Repetitions = {0}'.format(repeats))

    startTime = time.clock()
    for repeat in range(repeats):
        F = numerical.dft2(f)
    string = 'Average time per transform = {0:.8f} [s] '
    string += '({1}x{2}-point DFT2)'
    print(string.format((time.clock() - startTime)/repeats, M, N))

    startTime = time.clock()
    for repeat in range(repeats):
        F = numpy.fft.fft2(f)
    string = 'Average time per transform = {0:.8f} [s] '
    string += '({1}x{2}-point FFT2)'
    print(string.format((time.clock() - startTime)/repeats, M, N))
