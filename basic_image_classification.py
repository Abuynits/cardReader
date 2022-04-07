import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt


print(tf.__version__)

fashion_mnist = tf.keras.datasets.fashion_mnist
#return 4 nump arrays-  train images and train labels are training set- data the model ueses to learn
#tested against the test images and test labels
#labels are array of integers ranign from 0 to 9- correspond to clition represents
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
#how classify the data
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

print(train_images.shape)  #show the shape of the data.  wher 60000 is the length of the data

#each label is called 28x28 there train_labels contain the labels corresponding to the images

#there are 10k images in test set
print(test_images.shape)
