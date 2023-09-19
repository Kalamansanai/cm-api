
from datetime import datetime

from bson import ObjectId
from startup import mongo
from domain.detector import Detector

class Location():

    def __init__(self, location_json: dict):
        self.id = location_json["_id"]
        self.user_id: str = location_json["user_id"]
        self.name: str = location_json["name"]
        self.detectors: list[Detector] = [
            Detector(detector) for detector in location_json["detectors"]]
        self.monthly_logs: list[Monthly_log] = [
            Monthly_log(log) for log in location_json["monthly_logs"]]

    def get_db(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "detectors": [detector.get_db() for detector in self.detectors],
            "monthly_logs": [log.get_json() for log in self.monthly_logs]
        }

    def get_json(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "name": self.name,
            "detectors": [detector.get_json() for detector in self.detectors],
            "monthly_logs": [log.get_json() for log in self.monthly_logs]
        }

    def add_monthly_log(self, detector: Detector, new_value: int):
        date = f"{datetime.now().year}.{str(datetime.now().month).zfill(2)}"

        for log in self.monthly_logs:
            if log.month == date:
                log.values.add_value(detector.type, new_value)
                break
        else:
            self.monthly_logs.append(
                Monthly_log({
                    "month": date,
                    "values": {
                        "water": 0,
                        "electricity": 0,
                        "gas": 0
                    }
                })
            )
            self.monthly_logs[-1].values.add_value(detector.type, new_value)

        mongo.locations.update_one(
            {"_id": ObjectId(detector.location_id)},
            {"$set": self.get_db()}
        )

class Monthly_log():
    def __init__(self, log_json: dict):
        self.month = log_json["month"]
        self.values: Consumption_values = Consumption_values(
            log_json["values"])

    def get_json(self):
        return {
            "month": self.month,
            "values": self.values.get_json()
        }

class Consumption_values():
    def __init__(self, values_json: dict):
        self.water = values_json["water"]
        self.electricity = values_json["electricity"]
        self.gas = values_json["gas"]

    def get_json(self):
        return {
            "water": self.water,
            "electricity": self.electricity,
            "gas": self.gas
        }

    def add_value(self, type: str, new_value: int):
        if type == "water":
            self.water = self.water + new_value
        elif type == "electricity":
            self.electricity = self.electricity + new_value
        else:
            self.gas = self.gas + new_value
