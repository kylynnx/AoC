from abc import abstractmethod
from typing import Dict, Type, List

from range_gear import RangeGear


class RangeWorkflow:
    _name: str = None
    __registered_workflows: Dict[str, Type['RangeWorkflow']] = {}

    def __init_subclass__(cls, **kwargs):
        if cls._name is None:
            raise ValueError('Must set `_name`')

        RangeWorkflow.__registered_workflows[cls._name] = cls

    @staticmethod
    @abstractmethod
    def process(range_gear: RangeGear) -> List[RangeGear]:
        pass

    @staticmethod
    def get(name: str) -> Type['RangeWorkflow']:
        return RangeWorkflow.__registered_workflows[name]
