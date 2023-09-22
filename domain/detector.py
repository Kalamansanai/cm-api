from enum import Enum
from domain.log import Log
import json
import pandas as pd
from flask import request

class Detector():

    def __init__(self, detector_json: dict):
        self.id = detector_json["_id"]
        self.location_id = detector_json["location_id"]
        self.detector_id: str = detector_json["detector_id"]
        self.detector_name: str = detector_json["detector_name"]
        self.type: str = detector_json["type"]
        self.state: DetectorState = map_state(detector_json["state"])
        self.detector_config: DetectorConfig = DetectorConfig(
            detector_json["detector_config"])
        self.logs: list[Log] = [Log(log) for log in detector_json["logs"]]
        self.img_path: str = detector_json["img_path"]

    def get_db(self):
        return {
            "_id": self.id,
            "location_id": self.location_id,
            "detector_id": self.detector_id,
            "detector_name": self.detector_name,
            "type": str(self.type),
            "state": str(self.state),
            "detector_config": self.detector_config.get_json(),
            "logs": [log.get_json() for log in self.logs],
            "img_path": self.img_path
        }

    def get_json(self):
        return {
            "id": str(self.id),
            "location_id": str(self.location_id),
            "detector_id": self.detector_id,
            "detector_name": self.detector_name,
            "type": str(self.type),
            "state": str(self.state),
            "detector_config": self.detector_config.get_json(),
            "logs": [log.get_json() for log in self.logs],
            "img_path": self.img_path
        }

    def consumption_by_month(self, month: int):
        data = [log.get_json() for log in self.logs]
        if data == []:
            return 0

        df = pd.DataFrame.from_dict(data)
        df["month"] = pd.DatetimeIndex(df["timestamp"]).month

        df = df.loc[(df["month"] == month)]

        if df.empty:
            return 0

        return df.iloc[-1]["value"] - df.iloc[0]["value"]

def create_detector_for_mongo(detector_id: str, location_id: str, detector_name: str, char_num: int, coma_position: int, type: str):
    return {
        "detector_id": detector_id,
        "location_id": location_id,
        "detector_name": detector_name,
        "detector_config": {
            "delay": 86400000,  # a day
            "cost": 1,
            "flash": 0,
            "charNum": char_num,
            "comaPosition": coma_position
        },
        "type": type,
        "state": "init",
        "logs": [],
        "img_path": ""
    }

def detector_valid(detector_id: str):
    if detector_id not in json.load(open('library/detector_list.json'))["id"]:
        return False
    return True

class DetectorConfig():

    def __init__(self, config_json: dict):
        self.charNum = config_json["charNum"] if "charNum" in config_json.keys(
        ) else ""
        self.comaPosition = config_json["comaPosition"] if "comaPosition" in config_json.keys(
        ) else ""
        self.delay: int = config_json["delay"] if "delay" in config_json.keys(
        ) else 0
        self.cost: int = config_json["cost"] if "cost" in config_json.keys(
        ) else 0
        self.flash: int = config_json["flash"] if "flash" in config_json.keys(
        ) else 0

    def get_json(self):
        return {
            "charNum": self.charNum,
            "comaPosition": self.comaPosition,
            "delay": self.delay,
            "cost": self.cost,
            "flash": self.flash
        }

class DetectorState(Enum):
    INIT = 1
    SLEEP = 2

def map_state(state: str):
    if state == "init":
        return DetectorState.INIT
    elif state == "sleep":
        return DetectorState.SLEEP
    else:
        return DetectorState.INIT
