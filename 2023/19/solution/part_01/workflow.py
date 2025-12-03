from abc import abstractmethod
from typing import Type

from final_type import FinalType
from gear import Gear


class Workflow:
    _name: str = None
    __registered_rules = {}

    def __init_subclass__(cls, **kwargs):
        if not cls._name:
            raise ValueError('Must set `_name`')
        Workflow.__registered_rules[cls._name] = cls

    @staticmethod
    def get(name: str) -> Type['Workflow']:
        return Workflow.__registered_rules[name]

    @staticmethod
    @abstractmethod
    def process(gear: Gear) -> FinalType:
        pass
