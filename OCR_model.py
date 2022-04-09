import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist
import Rectangle


def init_model():
    print(tf.__version__)
    prediction_model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        # after flattened, consist of these 2 dense layers- fullyconnected neural layers.
        tf.keras.layers.Dense(128, activation='relu'),  # has 128 nodes
        tf.keras.layers.Dense(10)
        # has 10 nodes - returns logits array with 10 - each node has score indicate current image
    ])
    ((train_data, train_labels), (test_data, test_labels)) = mnist.load_data()
    print("training data shape:", train_data.shape)

    # convert to range 0 to 1
    train_data = train_data / 255.0
    test_data = test_data / 255.0
    prediction_model.compile(optimizer='adam',
                             loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                             metrics=['accuracy'])

    prediction_model.fit(train_data, train_labels, epochs=5)

    model_loss, model_accuracy = prediction_model.evaluate(test_data, test_labels, verbose=2)
    print('Model Accuracy:', model_accuracy)
    return prediction_model


def predict_image(rect, prediction_model):
    img = rect.greyscale_number_pixel_array

    np_img = np.expand_dims(img, 0)
    predictions_single = prediction_model.predict(np_img)
    print(predictions_single)
    print(np.argmax(predictions_single[0]))
    rect.card_number = np.argmax(predictions_single[0])
    return predictions_single, np.argmax(predictions_single[0])
