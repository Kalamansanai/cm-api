import cv2
import numpy as np
from cm_config import Logger
from ultralytics import YOLO


class _Detector:

    def __init__(self, plate_model_path, number_model_path):
        self.plates_model = YOLO(plate_model_path)
        self.number_model = YOLO(number_model_path)
        self.debug_img = None

    def detect(self, img, length, decimal, thr=0.4):
        img = self.detect_plates(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return None if img is None else self.detect_numbers(img, length, decimal, thr)

    def detect_plates(self, img):
        self.debug_img = img
        result = self.plates_model.predict(source=[img], verbose=False)[0]
        Logger.debug(f"Detected {len(result)} plate(s).")
        result.boxes.data = sorted(
            result.boxes.data, key=lambda x: x[4], reverse=True)

        for box in result.boxes:
            x1, y1, x2, y2 = np.round(box.xyxy[0].numpy()).astype(int)
            self.debug_img = [x1, y1, result.plot()]
            return img[y1:y2, x1:x2]
        return None

    def detect_numbers(self, img, length, decimal, thr):
        img = self.automatic_brightness_and_contrast(img)
        result = self.number_model.predict(source=[img], verbose=False)[0]
        (f"Detected {len(result)} number(s).")

        # Remove below threshold
        detections = []
        r = 0
        for row in result.boxes.data:
            if row[4] >= thr:
                detections.append(row)
            else:
                r += 1
        if r > 0:
            Logger.debug(f"Removed {r} image(s) below threshold ({thr}).")

        # Debug plot
        self.debug_img[2][self.debug_img[1]:self.debug_img[1]+result.plot().shape[0],
                          self.debug_img[0]:self.debug_img[0]+result.plot().shape[1]] = result.plot()
        self.debug_img = self.debug_img[2]
        cv2.imwrite("library/debug.png", self.debug_img)
        Logger.debug("Debug image saved.")

        # Not enough numbers found
        if len(detections) < length:
            Logger.debug("Not enough numbers detected for valid number.")
            return None

        # Sort by size and use first "length"s numbers
        r = len(detections) - length
        if r > 0:
            Logger.debug(
                f"Removed {r} less relevant number(s) from detection.")
        detections = sorted(
            detections, key=lambda x: x[2]*x[3], reverse=False)[:length]

        # Sort by X coordinate
        detections = sorted(detections, key=lambda x: x[0], reverse=False)

        # Create float number from list
        nums = [str(int(row[-1])) for row in detections]
        return int(''.join(nums)) / (10 ** decimal)

    def automatic_brightness_and_contrast(self, image, clip_hist_percent=1):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Calculate grayscale histogram
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        hist_size = len(hist)

        # Calculate cumulative distribution from the histogram
        accumulator = []
        accumulator.append(float(hist[0]))
        for index in range(1, hist_size):
            accumulator.append(accumulator[index - 1] + float(hist[index]))

        # Locate points to clip
        maximum = accumulator[-1]
        clip_hist_percent *= (maximum/100.0)
        clip_hist_percent /= 2.0

        # Locate left cut
        minimum_gray = 0
        while accumulator[minimum_gray] < clip_hist_percent:
            minimum_gray += 1

        # Locate right cut
        maximum_gray = hist_size - 1
        while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
            maximum_gray -= 1

        # Calculate alpha and beta values
        alpha = 255 / (maximum_gray - minimum_gray)
        beta = -minimum_gray * alpha

        auto_result = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
        auto_result = cv2.cvtColor(auto_result, cv2.COLOR_BGR2GRAY)
        auto_result = cv2.cvtColor(auto_result, cv2.COLOR_GRAY2RGB)
        return auto_result
