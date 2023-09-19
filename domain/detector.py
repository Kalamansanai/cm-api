from enum import Enum
from domain.log import Log

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
