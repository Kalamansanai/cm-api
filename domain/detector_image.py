class DetectorImage:
    def __init__(self, image_json: dict):
        self.id = image_json["_id"]
        self.detector_id: str = image_json["detector_id"]
        self.path: str = image_json["path"]

