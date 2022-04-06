from typing import Any
from abc import ABC, abstractmethod


class BaseConverter(ABC):

    @abstractmethod
    def export(self, input_filepath: str = '', output_filepath: str = '', option: dict[str, Any] = dict()):
        pass
