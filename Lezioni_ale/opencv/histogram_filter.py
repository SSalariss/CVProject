import numpy as np
import cv2
import matplotlib.pyplot as plt

# reading the image
img = cv2.imread("Esercitazioni\opencv_lessons\data\lena.png")


#? What is histogram?
# Is a visual rappresentation of quantitative datas
# We are calculation the distribution of each channel
# 256: how many 'groups' we have? one for each value
# [0, 255]: the range of possibles values
# [i] = the channel
color = ('b', 'g', 'r')
color_range = [0, 255]
diagram_range = [0, 255]
bin = [256]     # se fosse 64 avremmo che ogni bin copre 256 / 64 = 4 valori di intensità


for i, col in enumerate(color):
    #channel = img[:,:,i] only visual purpose
    #plt.hist(channel.ravel(), 256, [0, 255], color=col) only visual purpose
    hist = cv2.calcHist([img], [i], None, bin, color_range)
    plt.plot(hist, color=col)

plt.xlim(diagram_range) # the range of possibles values
plt.show()
