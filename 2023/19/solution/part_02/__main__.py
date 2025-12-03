from attribute_range import AttributeRange
from range_gear import RangeGear
from range_workflow import RangeWorkflow
from range_workflow_factory import RangeWorkflowFactory


def main(filename: str):
    with open(filename, 'r') as _f:
        content = _f.read()
        workflow_strings, _ = content.split('\n\n')

    _workflows = [RangeWorkflowFactory.deserialize(_) for _ in workflow_strings.split('\n')]

    in_workflow = RangeWorkflow.get('in')
    start = RangeGear(
        x_range=AttributeRange(start=1, end=4001),
        m_range=AttributeRange(start=1, end=4001),
        a_range=AttributeRange(start=1, end=4001),
        s_range=AttributeRange(start=1, end=4001),
        target=None
    )
    accepted = in_workflow.process(start)
    print(sum([_.combinations for _ in accepted]))


if __name__ == '__main__':
    main('../../input.txt')
