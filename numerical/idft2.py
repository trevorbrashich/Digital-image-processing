import numpy as np
import numerical

def idft2(F, scale=False):

   c = F.swapaxes(0,1)
   Columns = []
   for col in range(c.shape[0]):
      Columns.append(numerical.idft(c[col], False))

   x = np.array(Columns)

   r = x.swapaxes(0,1)
   Rows = []
   for row in range(r.shape[0]):
      Rows.append(numerical.idft(r[row], False))

   fU = np.array(Rows)

   M = F.shape[0]*F.shape[1]
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
    F = numpy.zeros((M,N), dtype=numpy.complex128)
    F[0,0] = 1

    repeats = 10
    print('Repetitions = {0}'.format(repeats))

    startTime = time.clock()
    for repeat in range(repeats):
        f = numerical.idft2(F)
    string = 'Average time per transform = {0:.8f} [s] '
    string += '({1}x{2}-point iDFT2)'
    print(string.format((time.clock() - startTime)/repeats, M, N))

    startTime = time.clock()
    for repeat in range(repeats):
        f = numpy.fft.ifft2(F)
    string = 'Average time per transform = {0:.8f} [s] '
    string += '({1}x{2}-point iFFT2)'
    print(string.format((time.clock() - startTime)/repeats, M, N))
