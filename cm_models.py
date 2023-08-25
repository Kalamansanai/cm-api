from enum import Enum
from datetime import date


class User():

    def __init__(self, user_json: dict):
        self.id = user_json["_id"]
        self.creation_time: str = user_json["creation_time"]
        self.name: str = user_json["name"]
        self.email: str = user_json["email"]
        self.password_salt: str = user_json["password_salt"]
        self.password_hash: str = user_json["password_hash"]
        self.config: dict = user_json["config"]

    def get_json(self):
        return {
            "id": str(self.id),
            "creation_time": self.creation_time,
            "name": self.name,
            "email": self.email,
            "config": self.config,
        }


class Location():

    def __init__(self, location_json: dict):
        self.id = location_json["_id"]
        self.user_id: str = location_json["user_id"]
        self.name: str = location_json["name"]
        self.detectors: list[Detector] = [
            Detector(detector) for detector in location_json["detectors"]]

    def get_json(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "name": self.name,
            "detectors": [detector.get_json() for detector in self.detectors]
        }


class Detector():

    def __init__(self, detector_json: dict):
        self.id = detector_json["_id"]
        self.location_id = detector_json["location_id"]
        self.detector_id: str = detector_json["detector_id"]
        self.detector_name: str = detector_json["detector_name"]
        self.type: DetectorType = map_type(detector_json["type"])
        self.state: DetectorState = map_state(detector_json["state"])
        self.detector_config: DetectorConfig = DetectorConfig(
            detector_json["detector_config"])
        self.logs: list[Log] = [Log(log) for log in detector_json["logs"]]
        self.img_path: str = detector_json["img_path"]

    def get_db(self):
        return {
            "id": self.id,
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


class DetectorConfig():

    def __init__(self, config_json: dict):
        self.charNum: int = config_json["charNum"] if "charNum" in config_json.keys(
        ) else ""
        self.comaPosition: int = config_json["comaPosition"] if "comaPosition" in config_json.keys(
        ) else ""
        self.delay: int = config_json["delay"] if "delay" in config_json.keys(
        ) else ""
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


class Log():

    def __init__(self, log_json: dict):
        self.timestamp: date = log_json["timestamp"]
        self.value = log_json["value"]

    def get_json(self):
        return {
            "timestamp": self.timestamp,
            "value": self.value
        }


def map_type(type: str):
    if type == "water":
        return DetectorType.WATER
    elif type == "gas":
        return DetectorType.GAS
    elif type == "electricity":
        return DetectorType.ELECTRICITY


class DetectorType(Enum):
    WATER = 1
    GAS = 2
    ELECTRICITY = 3


def map_state(state: str):
    if state == "init":
        return DetectorState.INIT
    elif state == "sleep":
        return DetectorState.SLEEP


class DetectorState(Enum):
    INIT = 1
    SLEEP = 2
