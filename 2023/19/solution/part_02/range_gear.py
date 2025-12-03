from typing import Union, Optional

from attribute_range import AttributeRange
from final_type import FinalType


class RangeGear:
    def __init__(
        self, x_range: AttributeRange, m_range: AttributeRange, a_range: AttributeRange, s_range: AttributeRange,
        target: Optional[Union[str, FinalType]]
    ):
        self._x_range = x_range
        self._m_range = m_range
        self._a_range = a_range
        self._s_range = s_range
        self._target = target

    @property
    def x_range(self):
        return self._x_range

    @property
    def m_range(self):
        return self._m_range

    @property
    def a_range(self):
        return self._a_range

    @property
    def s_range(self):
        return self._s_range

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = value

    @property
    def combinations(self):
        return self._x_range.range * self._m_range.range * self._a_range.range * self._s_range.range

    def copy(self):
        return RangeGear(
            x_range=AttributeRange(start=self._x_range.start, end=self._x_range.end),
            m_range=AttributeRange(start=self._m_range.start, end=self._m_range.end),
            a_range=AttributeRange(start=self._a_range.start, end=self._a_range.end),
            s_range=AttributeRange(start=self._s_range.start, end=self._s_range.end),
            target=self._target
        )
