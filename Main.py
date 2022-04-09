import math
from random import randint

import numpy as np
import cv2
import OCR_model
import image_processing

threshold_value = 170
min_area = 50000
max_area = 10000000
image_name = "cards.JPG"
rectangle_list = []
img = cv2.imread(image_name)
image_processing.find_rectangle_contours(img, threshold_value, min_area, max_area, rectangle_list)
image_processing.find_greyscale_number_array(img, rectangle_list)

prediction_model=OCR_model.init_model()
for rect in rectangle_list:
    OCR_model.predict_image(rect,prediction_model)

image_processing.update_rectangle_values(rectangle_list,img)
cv2.imshow('cards', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
