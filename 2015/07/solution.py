import re
from abc import abstractmethod
from enum import Enum
from typing import Type


class Operator(Enum):
    OR = "OR"
    AND = "AND"
    NOT = "NOT"
    LEFT = "LSHIFT"
    RIGHT = "RSHIFT"
    THROUGH = "none"
    NON_EXISTENT = "non_existent"


def try_int_cast(string: str) -> int | str:
    try:
        return int(string)
    except (ValueError, TypeError):
        return string


class WireState:
    _wires = {}

    @staticmethod
    def set_wire_input(name: str, value: int):
        WireState._wires[name] = value

    @staticmethod
    def get_wire(name: str):
        return WireState._wires[name]


class WireSource:
    _operator: Operator = None
    __registered_wires: dict[Operator, Type['WireSource']] = {}
    _target: str = None

    def __init__(self, wiring_str: str):
        self._target = WireSource.get_target(wiring_str)
        self._signal = None

    @property
    def target(self):
        return self._target

    def get_signal(self) -> int:
        if not self._signal:
            self._set_signal()

        return self._signal

    def reset(self):
        self._signal = None

    @abstractmethod
    def _set_signal(self):
        pass

    @staticmethod
    def get_target(wiring_str: str) -> str:
        return re.match(r".* -> ([a-z]{1,2})$", wiring_str).group(1)

    def __init_subclass__(cls, **kwargs):
        if cls._operator is None:
            raise ValueError("Must set `_operator` attribute")
        WireSource.__registered_wires[cls._operator] = cls

    @staticmethod
    def from_string(wiring_str: str) -> "WireSource":
        if Operator.AND.value in wiring_str:
            return WireSource.__registered_wires[Operator.AND](wiring_str)
        elif Operator.OR.value in wiring_str:
            return WireSource.__registered_wires[Operator.OR](wiring_str)
        elif Operator.NOT.value in wiring_str:
            return WireSource.__registered_wires[Operator.NOT](wiring_str)
        elif Operator.LEFT.value in wiring_str:
            return WireSource.__registered_wires[Operator.LEFT](wiring_str)
        elif Operator.RIGHT.value in wiring_str:
            return WireSource.__registered_wires[Operator.RIGHT](wiring_str)
        return WireSource.__registered_wires[Operator.THROUGH](wiring_str)

    @staticmethod
    def get_signal_by_reference(reference):
        if isinstance(reference, int):
            return reference

        return CombineWire.get_signal(reference)


class WireSourceDual(WireSource):
    _operator = Operator.NON_EXISTENT

    def __init__(self, wiring_str: str):
        super().__init__(wiring_str)
        self._left, self._right = self.get_left_and_right(wiring_str)

    def get_left_and_right(self, wiring_str: str) -> (str, str):
        source_group = r"([0-9]{1,5}|[a-z]{1,2})"
        target = r"[a-z]{1,2}"
        match = re.match(
            fr"^{source_group} {self._operator.value} {source_group} -> {target}$",
            wiring_str
        )

        return try_int_cast(match.group(1)), try_int_cast(match.group(2))

    def _set_signal(self):
        left = WireSource.get_signal_by_reference(self._left)
        right = WireSource.get_signal_by_reference(self._right)
        self._signal = self._operate(left, right)

    @staticmethod
    @abstractmethod
    def _operate(left, right):
        pass


class WireSourceOR(WireSourceDual):
    _operator = Operator.OR

    @staticmethod
    def _operate(left, right):
        return left | right


class WireSourceAND(WireSourceDual):
    _operator = Operator.AND

    @staticmethod
    def _operate(left, right):
        return left & right


class WireSourceLEFT(WireSourceDual):
    _operator = Operator.LEFT

    @staticmethod
    def _operate(left, right):
        return left << right


class WireSourceRIGHT(WireSourceDual):
    _operator = Operator.RIGHT

    @staticmethod
    def _operate(left, right):
        return left >> right


class WireSourceNOT(WireSource):
    _operator = Operator.NOT

    def __init__(self, wiring_str: str):
        super().__init__(wiring_str)
        match = re.match(r"^NOT ([a-z]{1,2}) -> [a-z]{1,2}$", wiring_str)
        self._source = match.group(1)

    def _set_signal(self):
        self._signal = ~WireSource.get_signal_by_reference(self._source)


class WireSourceThrough(WireSource):
    _operator = Operator.THROUGH

    def __init__(self, wiring_str: str):
        super().__init__(wiring_str)
        match = re.match(r"^([a-z]{1,2}) -> [a-z]{1,2}$", wiring_str)
        self._source = match.group(1)

    def _set_signal(self):
        self._signal = WireSource.get_signal_by_reference(self._source)


class CombineWire:
    _targets: dict[str, WireSource] = {}

    @staticmethod
    def set_input(name: str, wire_input: WireSource):
        CombineWire._targets[name] = wire_input

    @staticmethod
    def get_signal(name: str):
        if name in CombineWire._targets:
            return CombineWire._targets[name].get_signal()

        return WireState.get_wire(name)

    @staticmethod
    def reset():
        for wire in CombineWire._targets.values():
            wire.reset()


def read_wirings(wiring_strings: list[str]):
    for wiring in wiring_strings:
        if match := re.match(r"^([0-9]{1,5}) -> ([a-z]{1,2})$", wiring):
            WireState.set_wire_input(name=match.group(2), value=int(match.group(1)))
        else:
            _wire = WireSource.from_string(wiring)
            CombineWire.set_input(_wire.target, _wire)


def main(filename: str):
    with open(filename) as f:
        wiring_strings = f.readlines()

    read_wirings(wiring_strings)

    signal_a = CombineWire.get_signal("a")
    print(signal_a)

    WireState.set_wire_input("b", signal_a)
    CombineWire.reset()
    print(CombineWire.get_signal("a"))


if __name__ == '__main__':
    main("input.txt")
