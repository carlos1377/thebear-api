from abc import ABC, abstractmethod


class Repository(ABC):

    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def id_one_or_404(self, _id):
        raise NotImplementedError

    @abstractmethod
    def save(self, _object):
        raise NotImplementedError

    @abstractmethod
    def remove(self, _object):
        raise NotImplementedError

    @abstractmethod
    def update_object(self, _id, _object_dump):
        raise NotImplementedError
