from datetime import datetime

class Log():

    def __init__(self, log_json: dict):
        self.timestamp: datetime = log_json["timestamp"]
        self.value = log_json["value"]

    def get_json(self):
        return {
            "timestamp": self.timestamp,
            "value": self.value
        }
