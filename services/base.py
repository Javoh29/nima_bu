from abc import ABC, abstractmethod

class BaseService(ABC):
    @abstractmethod
    def search(self, *args, **kwargs):
        pass 