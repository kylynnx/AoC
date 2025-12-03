import operator
import re
from typing import Callable, Tuple, Union

from final_type import FinalType
from gear import Gear
from workflow import Workflow


class WorkflowFactory:
    @staticmethod
    def deserialize(workflow_string: str):
        match = re.match(r'([a-z]{1,3}){(.+)}', workflow_string)
        process_func = WorkflowFactory.get_process_func(match.group(2))
        name = match.group(1)
        return type(f'Workflow_{name}', (Workflow,), {'_name': name, 'process': staticmethod(process_func)})

    @staticmethod
    def get_process_func(process_string: str) -> Callable[[Gear], FinalType]:
        steps = process_string.split(',')
        operation_functions = []
        for step in steps[:-1]:
            operation_functions.append(WorkflowFactory.deserialize_step(step))

        fallback_target = WorkflowFactory.get_target(steps[-1])

        def process(gear: Gear) -> FinalType:
            for f, t in operation_functions:
                if f(gear):
                    if isinstance(t, str):
                        return Workflow.get(t).process(gear)
                    else:
                        return t

            if isinstance(fallback_target, str):
                return Workflow.get(fallback_target).process(gear)
            else:
                return fallback_target

        return process

    @staticmethod
    def get_operation(attribute: str, operation: str, value: int) -> Callable[[Gear], bool]:
        if operation == '>':
            def func(gear: Gear) -> bool:
                return operator.attrgetter(attribute)(gear) > value
        else:
            def func(gear: Gear) -> bool:
                return operator.attrgetter(attribute)(gear) < value

        return func

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
    def deserialize_step(step: str) -> Tuple[Callable[[Gear], bool], Union[FinalType, str]]:
        condition, target_string = step.split(':')
        match = re.match('([xmas])([<>])([0-9]+)', condition)
        func = WorkflowFactory.get_operation(
            attribute=match.group(1),
            operation=match.group(2),
            value=int(match.group(3))
        )
        target = WorkflowFactory.get_target(target_string)

        return func, target
