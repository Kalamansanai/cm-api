import cv2
import numpy as np
from cm_config import Logger
from ultralytics import YOLO

class _Detector:

    def __init__(self, plate_model_path, number_model_path):
        self.plates_model = YOLO(plate_model_path)
        self.number_model = YOLO(number_model_path)

    def detect(self, img, length, decimal, id, thr=0.4):
        img, orig, coords = self.detect_plates(img)
        
        ret = None
        if img is not None:
            ret, orig = self.detect_numbers(img, length, decimal, coords, orig, thr)

        cv2.imwrite(f"library/images/{id}.png", cv2.cvtColor(orig, cv2.COLOR_BGR2RGB))
        return ret

    def detect_plates(self, img):
        result = self.plates_model.predict(source=[img], verbose=False)[0]
        Logger.info(f"Detected {len(result)} plate(s).")
        result.boxes.data = sorted(
            result.boxes.data, key=lambda x: x[4], reverse=False)

        ret_img = None
        x1, y1 = None, None
        for i, box in enumerate(result.boxes):
            x1, y1, x2, y2 = np.round(box.xyxy[0].numpy()).astype(int)
            ret_img = img[y1:y2, x1:x2]
            img = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0) if i+1 == len(result.boxes) else (255, 0, 0), 2)
            
        return ret_img, img, (x1, y1)

    def detect_numbers(self, img, length, decimal, coords, orig, thr):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = self.automatic_brightness_and_contrast(img)
        result = self.number_model.predict(source=[img], verbose=False)[0]
        (f"Detected {len(result)} number(s).")

        # Sort by X coordinate
        result.boxes.data = sorted(result.boxes.data, key=lambda x: x[0], reverse=False)

        # Remove below threshold
        detections = []
        r = 0
        for box in result.boxes:
            x1, y1, x2, y2 = np.round(box.xyxy[0].numpy()).astype(int)
            if box.data[0][4] >= thr:
                if len(detections) < length:
                    detections.append(box.data[0])
                    orig = cv2.rectangle(orig, (x1+coords[0], y1+coords[1]), (x2+coords[0], y2+coords[1]), (0, 255, 0), 2)
                else:
                    orig = cv2.rectangle(orig, (x1+coords[0], y1+coords[1]), (x2+coords[0], y2+coords[1]), (255, 0, 0), 2)
            else:
                r += 1
                orig = cv2.rectangle(orig, (x1+coords[0], y1+coords[1]), (x2+coords[0], y2+coords[1]), (255, 255, 0), 2)
        if r > 0:
            Logger.info(f"Removed {r} image(s) below threshold ({thr}).")

        # TODO egymás alattiakat ne fogadjon el, csak egymás mellettieket

        # Create float number from list
        value = int(''.join([str(int(row[-1])) for row in detections])) / (10 ** decimal)
            
        # Not enough numbers found
        if len(detections) < length:
            Logger.info("Not enough numbers detected for valid number.")
            orig = cv2.putText(orig, f"Detected value: {value}", (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 4, cv2.LINE_AA)
            return None, orig
        orig = cv2.putText(orig, f"Detected value: {value}", (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 4, cv2.LINE_AA)

        return value, orig
        

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