# app/repository/repository_interface.py
from abc import ABC, abstractmethod

class IRepository(ABC):
    @abstractmethod
    def add(self, entity):
        pass

    @abstractmethod
    def get_by_id(self, entity_id):
        pass

    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def delete(self, entity_id):
        pass
