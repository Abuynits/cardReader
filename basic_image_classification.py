import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

print(tf.__version__)

fashion_mnist = tf.keras.datasets.fashion_mnist
# return 4 nump arrays-  train images and train labels are training set- data the model ueses to learn
# tested against the test images and test labels
# labels are array of integers ranign from 0 to 9- correspond to clition represents
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
# how classify the data
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

print(train_images.shape)  # show the shape of the data.  wher 60000 is the length of the data

# each label is called 28x28 there train_labels contain the labels corresponding to the images

# there are 10k images in test set
print(test_images.shape)


def showImage():
    plt.figure()
    plt.imshow(train_images[0])
    plt.colorbar()
    plt.grid(False)
    plt.show()


# showImage()

# need to move the model into range of 0 to 1
train_images = train_images / 255.0

test_images = test_images / 255.0


def displayFirst25():
    plt.figure(figsize=(10, 10))
    for i in range(25):
        plt.subplot(5, 5, i + 1)  # only display in certain region
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(train_images[i], cmap=plt.cm.binary)  # show the image in the subplot
        plt.xlabel(class_names[train_labels[i]])  # label the image with the train label
    plt.show()  # after looping, show the plot in grey scale


# displayFirst25()

# Layers - basic building block
# extract representations from data fed into them

model = tf.keras.Sequential([
    # first layer: transforms format from 2D 28x28 to 1D of 784 (28*28) - just unstack the data- no parameter to learn
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    # after flattened, consist of these 2 dense layers- fullyconnected neural layers.
    tf.keras.layers.Dense(50, activation='relu'),  # has 128 nodes
    tf.keras.layers.Dense(10)
    # has 10 nodes - returns logits array with 10 - each node has score indicate current image

])

# loss function: measure of how accurate the model is during training
# optimizer: how model is updated based on data it sees and its loss function
# metrics: used to monitor training and testing steps
# the metric below is based on accuracy:
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# training: has 4 steps:
# 1: feed training data to the model- images and the labels
# 2: model learns to associate images and labels
# 3: ask model to make predictions about a test set - test_images
# 4: verify the predictions match the labesl for test_labels

# fits the model to the training data
model.fit(train_images, train_labels, epochs=5)

# Evaluate accuracy:
# compare how model performs on testing data
test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)

print('\nTest accuracy:', test_acc)

# if accuracy of training data is < accuracy of testing data, result is overfitting

# making predictions:

probability_model = tf.keras.Sequential([model,
                                         tf.keras.layers.Softmax()])

predictions = probability_model.predict(test_images)#the output testing on the images

print(predictions[0])#print the prediction for the first image

print(np.argmax(predictions[0]))#print the label that corresponds to class prediction

#how to use the trained model
# grab an image from the test dataset
img = test_images[1]
print(img.shape)
#add the image to batc where it's the only member:
# Add the image to a batch where it's the only member.
img = (np.expand_dims(img,0))

print(img.shape)

predictions_single = probability_model.predict(img)
print(predictions_single)

print(np.argmax(predictions_single[0]))