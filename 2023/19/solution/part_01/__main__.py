from final_type import FinalType
from gear import Gear
from workflow import Workflow
from workflow_factory import WorkflowFactory


def main(filename: str):
    with open(filename, 'r') as _f:
        content = _f.read()
        workflow_strings, gear_strings = content.split('\n\n')

    gears = [Gear(_) for _ in gear_strings.split('\n')]
    _workflows = [WorkflowFactory.deserialize(_) for _ in workflow_strings.split('\n')]

    start = Workflow.get('in')
    accepted = []

    for gear in gears:
        if start.process(gear) is FinalType.ACCEPTED:
            accepted.append(gear)

    print(sum([_.xmas for _ in accepted]))


if __name__ == '__main__':
    main('../../input.txt')
