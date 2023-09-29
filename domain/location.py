class Location():

    def __init__(self, location_json: dict):
        self.id = location_json["_id"]
        self.user_id: str = location_json["user_id"]
        self.name: str = location_json["name"]

    def get_db(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
        }

    def get_json(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "name": self.name,
        }

