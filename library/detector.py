import cv2
import random
from ultralytics import YOLO
import matplotlib.pyplot as plt
import numpy as np

class Detector:

    def __init__(self, plate_model_path, number_model_path):
        self.plates_model = YOLO(plate_model_path)
        self.number_model = YOLO(number_model_path)
        print("Models laoded")


    def detect(self, img, length, decimal):
        nums = []
        for img in self.detect_plates(img):
            nums.append(self.detect_numbers(img, length, decimal))

        return None if len(nums) < 1 else nums[0]

    def detect_plates(self, img):
        imgs = []
        results = self.plates_model.predict(source=[img])
        print(f"Detector found {len(results[0])} number plates")
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = np.round(box.xyxy[0].numpy()).astype(int)
                imgs.append(img[y1:y2, x1:x2])
        return imgs


    def detect_numbers(self, img, length, decimal):
        # results = self.number_model.predict(source=[img])
        # found = len(results[0])
        # print(f"Detector found {found} numbers on plate.")
        # if found != length:
        #     print(f"It should be {length}")
        #     return None
        # else:
        #     for result in results:
        #         for box in result.boxes:
        #             x1, y1, x2, y2 = np.round(box.xyxy[0].numpy()).astype(int)
        #             tmp = img[y1:y2, x1:x2]
        #             plt.imshow(tmp)
        #             plt.plot()
        #             plt.pause(10)


        return self.rnd(length, decimal)


    def rnd(self, digits, dec):
        min_value = 10 ** (digits - 1)
        max_value = 10 ** digits - 1
        dec = 10 ** dec
        random_float = random.randint(min_value, max_value)
        return random_float / dec



# d = Detector("library/plates.pt", "library/numbers.pt")
# a = d.detect(cv2.imread("library/test.jpg"), 8, 3)
# print(a)