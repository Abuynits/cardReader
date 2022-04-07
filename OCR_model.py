import numpy as np
from tensorflow.keras.datasets import mnist
#if given an image, need to split up in such a way so that I could search different sizes
# ie should I go with
#split into rowxcollumn. Then I loop over the r&c sections.
#need to run edge detection to find the top of each card.

#what if find the top and bottom of each card, then I look for lines that could be drawm
#only interested in reading numbers

#let the first step be to find the actual card, their dimensions. then given the H&W, I can map accordingly to find the area with the number
#if I find the area of the number, then I will be able to run it through tensor flow
((train_data, train_Labels), (test_data, test_labels)) = mnist.load_data()
