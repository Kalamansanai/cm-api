from api.api_utils import hash as _hash

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

    def same_password(self, psw: str):
        hash = _hash(psw + self.password_salt)
        if self.password_hash == hash:
            return True
        return False
                

def data_for_db_creation(creation_time: int, name: str, email: str, password_salt: str, password_hash: str, token: str):
    return {
        "creation_time": creation_time,
        "name": name,
        "email": email,
        "password_salt": password_salt,
        "password_hash": password_hash,
        "email_verification_token": token,
        "config": {},
    }

