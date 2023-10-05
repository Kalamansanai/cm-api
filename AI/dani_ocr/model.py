import cv2
import time
import numpy as np
from cm_config import IMAGE_PATH, Logger
from ultralytics import YOLO

from domain.model import Model
from AI.dani_ocr.validator import validate


class DaniOCR(Model):
    def __init__(self, model_paths: list[str]):
        self.plates_model = YOLO(model_paths[0])
        self.number_model = YOLO(model_paths[1])

    def validate(self, data):
        return validate(data)

    def detect(self, img, length, decimal, id, thr=0.8):
        cv2.imwrite(
            f"{IMAGE_PATH}/{round(time.time() * 1000)}.png",
            cv2.cvtColor(img, cv2.COLOR_BGR2RGB),
        )
        img, orig, coords = self.detect_plates(img)

        ret = None
        if img is not None:
            ret, orig = self.detect_numbers(img, length, decimal, coords, orig, thr)
        else:
            Logger.info("No detection")

        cv2.imwrite(f"{IMAGE_PATH}/{id}.png", cv2.cvtColor(orig, cv2.COLOR_BGR2RGB))
        return ret

    def detect_plates(self, img):
        result = self.plates_model.predict(source=[img], verbose=False)[0]
        Logger.info(f"Detected {len(result)} plate(s).")
        result.boxes.data = sorted(result.boxes.data, key=lambda x: x[4], reverse=False)

        ret_img = None
        x1, y1 = None, None
        for i, box in enumerate(result.boxes):
            x1, y1, x2, y2 = np.round(box.xyxy[0].numpy()).astype(int)
            ret_img = img[y1:y2, x1:x2]
            img = cv2.rectangle(
                img,
                (x1, y1),
                (x2, y2),
                (0, 255, 0) if i + 1 == len(result.boxes) else (255, 0, 0),
                2,
            )

        return ret_img, img, (x1, y1)

    def detect_numbers(self, img, length, decimal, coords, orig, thr):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
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
                    if len(detections) > 0:
                        if abs(box.data[0][0] - detections[-1][0]) > (
                            self.avg_dist(detections) / 2
                        ):
                            detections.append(box.data[0])
                            orig = cv2.rectangle(
                                orig,
                                (x1 + coords[0], y1 + coords[1]),
                                (x2 + coords[0], y2 + coords[1]),
                                (0, 255, 0),
                                2,
                            )
                        else:
                            r += 1
                            orig = cv2.rectangle(
                                orig,
                                (x1 + coords[0], y1 + coords[1]),
                                (x2 + coords[0], y2 + coords[1]),
                                (0, 0, 255),
                                2,
                            )
                    else:
                        detections.append(box.data[0])
                        orig = cv2.rectangle(
                            orig,
                            (x1 + coords[0], y1 + coords[1]),
                            (x2 + coords[0], y2 + coords[1]),
                            (0, 255, 0),
                            2,
                        )
                else:
                    r += 1
                    orig = cv2.rectangle(
                        orig,
                        (x1 + coords[0], y1 + coords[1]),
                        (x2 + coords[0], y2 + coords[1]),
                        (255, 0, 0),
                        2,
                    )
            else:
                r += 1
                orig = cv2.rectangle(
                    orig,
                    (x1 + coords[0], y1 + coords[1]),
                    (x2 + coords[0], y2 + coords[1]),
                    (255, 255, 0),
                    2,
                )

        if r > 0:
            Logger.info(f"Removed {r} image(s) below threshold ({thr}).")

        # Create float number from list
        if len(detections) > 0:
            value = int("".join([str(int(row[-1])) for row in detections])) / (
                10**decimal
            )
        else:
            value = None

        # Not enough numbers found
        if len(detections) < length:
            Logger.info("Not enough numbers detected for valid number.")
            orig = cv2.putText(
                orig,
                f"Detected value: {value}",
                (25, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (255, 0, 0),
                4,
                cv2.LINE_AA,
            )
            return None, orig
        orig = cv2.putText(
            orig,
            f"Detected value: {value}",
            (25, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (0, 255, 0),
            4,
            cv2.LINE_AA,
        )

        return value, orig

    def avg_dist(self, data):
        avg = 0
        for i in range(1, len(data)):
            prev = data[i - 1].numpy()
            act = data[i].numpy()
            avg += abs(act.data[0] - prev[0])

        return avg / len(data)
