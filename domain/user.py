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

