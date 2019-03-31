from abc import ABC, abstractmethod
from typing import Mapping, Any


_no_default = NotImplementedError('No default implementation in base Serializer class')


class Serializer(ABC):
    """
    Abstract base class for Serializer.
    Provides :meth:`serialize` method
    which should be implemented by subclasses.
    """

    @abstractmethod
    def serialize(self, message_attributes: Mapping[str, Any]) -> Any:
        raise _no_default
