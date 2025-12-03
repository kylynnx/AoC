import operator
import re
from typing import Callable, List, Union, Tuple

from final_type import FinalType
from range_gear import RangeGear
from range_workflow import RangeWorkflow


class RangeWorkflowFactory:
    @staticmethod
    def deserialize(workflow_string: str):
        match = re.match(r'([a-z]{1,3}){(.+)}', workflow_string)
        process_func = RangeWorkflowFactory.get_process_func(match.group(2))
        name = match.group(1)
        return type(f'Workflow_{name}', (RangeWorkflow,), {'_name': name, 'process': staticmethod(process_func)})

    @staticmethod
    def get_process_func(process_string: str) -> Callable[[RangeGear], List[RangeGear]]:
        steps = process_string.split(',')
        step_functions = []
        for step in steps[:-1]:
            step_functions.append(RangeWorkflowFactory.deserialize_step(step))

        fallback_target = RangeWorkflowFactory.get_target(steps[-1])

        def process(range_gear: RangeGear) -> List[RangeGear]:
            _accepted = []
            _current = range_gear
            for step_function in step_functions:
                _next, _current = step_function(_current)

                if isinstance(_next.target, str):
                    _accepted += RangeWorkflow.get(_next.target).process(_next)

                elif _next.target is FinalType.ACCEPTED:
                    _accepted.append(_next)

            if isinstance(fallback_target, str):
                _accepted += RangeWorkflow.get(fallback_target).process(_current)

            elif fallback_target is FinalType.ACCEPTED:
                _accepted.append(_current)

            return _accepted

        return process

    @staticmethod
    def get_target(target_string: str) -> Union[FinalType, str]:
        target_match = re.match(r'([AR])', target_string)
        if target_match:
            target = FinalType(target_match.group(1))
        else:
            target_match = re.match(r'([a-z]+)', target_string)
            target = target_match.group(1)
        return target

    @staticmethod
    def deserialize_step(step_string: str):
        condition, target_string = step_string.split(':')
        match = re.match('([xmas])([<>])([0-9]+)', condition)
        target = RangeWorkflowFactory.get_target(target_string)
        func = RangeWorkflowFactory.get_step_function(
            attribute=f'{match.group(1)}_range',
            operation=match.group(2),
            value=int(match.group(3)),
            target=target
        )
        return func

    @staticmethod
    def get_step_function(
        attribute: str, operation: str, value: int, target: Union[FinalType, str]
    ) -> Callable[[RangeGear], Tuple[RangeGear, RangeGear]]:
        def func(range_gear: RangeGear) -> Tuple[RangeGear, RangeGear]:
            _new_gear = range_gear.copy()
            _new_gear.target = target

            if operation == '>':
                operator.attrgetter(attribute)(_new_gear).start = value + 1
                operator.attrgetter(attribute)(range_gear).end = value + 1
            else:
                operator.attrgetter(attribute)(_new_gear).end = value
                operator.attrgetter(attribute)(range_gear).start = value

            return _new_gear, range_gear

        return func
