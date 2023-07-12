import cv2
import random
from ultralytics import YOLO

class Detector:

    def __init__(self, model_path):
        self.model = YOLO(model_path)


    def detect(self, img, length, decimal):
        return self.ocr(img, length, decimal) # DEV

        # img = self.preprocess(img)

        # results = self.model.predict(source=[img])
        # print(f"Detector found {len(results)} meters")
        # for result in results:
        #     for box in result.boxes:
        #         x, y, w, h = box.xywh[0]
        #         crop_img = img[int(y):int(y+h), int(x):int(x+w)]

        #         num = self.ocr(crop_img, length, decimal)
        #         if num != None:
        #             return num
        # return None

    def ocr(self, img, length, decimal):
        return self.rnd(length, decimal)

    def preprocess(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img

    def rnd(self, digits, dec):
        min_value = 10 ** (digits - 1)
        max_value = 10 ** digits - 1
        dec = 10 ** dec
        random_float = random.randint(min_value, max_value)
        return random_float / dec