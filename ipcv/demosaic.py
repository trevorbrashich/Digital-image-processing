import time
import rawpy
import numpy as np
from matplotlib import pyplot
from scipy.ndimage.filters import convolve

RED_CH   = 0
GREEN_CH = 1
BLUE_CH  = 2

even = lambda x: x%2==0
odd  = lambda x: x%2!=0

def cfa_channel(row, column):
    """Return color channel of row,column pair based on the Bayer filter."""

    # CR2 CFA Pattern: [Red   , Green] <-- even rows: 0, 2, 4, ...
    #                  [Green , Blue]  <-- odd  rows: 1, 3, 5, ...
    # Note: Python is zero-indexed

    if even(row):
        if even(column):
            return GREEN_CH
        return RED_CH
    else:
        if even(column):
            return BLUE_CH
        return GREEN_CH

path = './Raw.DNG'
with rawpy.imread(path) as raw:
    # np array with raw intensities values
    print('Copying img array')
    img = raw.raw_image.copy()
    # get WB as shot by the camera
    camera_wb = raw.camera_whitebalance

# print some info
(h, w) = img.shape
print(f'width x height: {w}x{h}')

print('Start demosaicing - Bilinear interpolation')
start_time = time.time()

print('Building channel masks...')
channels = dict((channel, np.zeros(img.shape)) for channel in 'RGB')
for channel, (y, x) in zip('RGGB', [(0, 0), (0, 1), (1, 0), (1, 1)]):
    channels[channel][y::2, x::2] = 1
R_m, G_m, B_m = tuple(channels[c].astype(bool) for c in 'RGB')

# convolution kernels
# green
H_G = np.asarray(
    [[0, 1, 0],
     [1, 4, 1],
     [0, 1, 0]]) / 4
# red/blue
H_RB = np.asarray(
    [[1, 2, 1],
     [2, 4, 2],
     [1, 2, 1]]) / 4

print('Running bilinear interpolation...')
R = convolve(img * R_m, H_RB)
G = convolve(img * G_m, H_G)
B = convolve(img * B_m, H_RB)
print('Stacking channels...')
rgb = np.dstack((R,G,B))

elapsed_time = time.time() - start_time
print('Elapsed time:', elapsed_time)

print('Normalizing from 0..65535 to 0..1 ...')
rgb = rgb / 65535

print('White balancing...')
white = np.array(camera_wb[:3])/65535
print('Reference white:', white)

final = rgb * white

print('Normalizing from 0..1 to 0..255 ...')
rgb = rgb * 255
final = final * 255
print('Applying gamma encoding (gamma = 1/2.2)...')
final = final ** (1/2.2)

print("Display final image...")
pyplot.title(r'Bilinear interpolation, white balance, $\gamma = \frac{1}{2.2}$')
pyplot.imshow(final, aspect='equal', interpolation='none')

# Uncomment the following lines to show individual channels
# zeros = np.zeros(final.shape, dtype=final.dtype)
# red = final * R_m
# green = final * G_m
# blue = final * B_m
# pyplot.figure()
# pyplot.title('Red channel')
# pyplot.imshow(np.dstack((red, zeros, zeros)), aspect='equal', interpolation='none')
# pyplot.figure()
# pyplot.title('Green channel')
# pyplot.imshow(np.dstack((zeros, green, zeros)), aspect='equal', interpolation='none')
# pyplot.figure()
# pyplot.title('Blue channel')
# pyplot.imshow(np.dstack((zeros, zeros, blue)), aspect='equal', interpolation='none')

pyplot.show()
