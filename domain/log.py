from datetime import datetime


class Log:
    def __init__(self, log_json: dict):
        self.location_id: str = log_json["location_id"]
        self.detector_id: str = log_json["detector_id"]
        self.type: str = log_json["type"]
        self.timestamp: datetime = log_json["timestamp"]
        self.value = log_json["value"]
        self.cost: int = log_json["cost"]

    def get_json(self):
        return {
            "location_id": self.location_id,
            "detector_id": self.detector_id,
            "type": self.type,
            "timestamp": self.timestamp,
            "value": self.value,
            "cost": self.cost,
        }
