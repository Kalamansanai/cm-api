from abc import ABC, abstractmethod


class Model(ABC):
    @abstractmethod
    def __init__(self, model_paths: list[str]):
        pass

    @abstractmethod
    def detect(self):
        pass

    @abstractmethod
    def validate(self, data):
        pass
