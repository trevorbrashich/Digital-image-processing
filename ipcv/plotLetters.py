import matplotlib.pyplot as plt
import cv2
import numpy as np
def plotLetters(histogram, letters):
    pos = np.arange(len(letters))
    width = 1.0     # gives histogram aspect to the bar diagram

    ax = plt.axes()
    ax.set_xticks(pos + (width / 2))
    ax.set_xticklabels(letters)

    plt.bar(pos, histogram, width, color='r')
    plt.show()
