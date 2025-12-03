from collections import defaultdict
from collections.abc import Callable


class BaseMachine:
    def __init__(self):
        self._registers: dict[str, int] = defaultdict(int)

    def get_value(self, value: str) -> int:
        try:
            return int(value)
        except ValueError:
            return self._registers[value]

    def set(self, register: str, value: str | int):
        self._registers[register] = self.get_value(value)

        return 1


    def add(self, register: str, value: str | int):
        self._registers[register] += self.get_value(value)

        return 1

    def mul(self, register: str, value: str | int):
        self._registers[register] *= self.get_value(value)

        return 1

    def mod(self, register: str, value: str | int):
        self._registers[register] %= self.get_value(value)

        return 1

    def jgz(self, register: str | int, value: str | int):
        if self.get_value(register) > 0:
            return self.get_value(value)

        return 1


class SoloMachine(BaseMachine):
    def __init__(self):
        super().__init__()
        self.signal = None
        self.received = False

    def snd(self, register: str):
        self.signal = self.get_value(register)

        return 1

    def rcv(self, register: str):
        if self.get_value(register) != 0:
            self.received = True
            return None

        return 1

    def run(self, program: list[str]):
        pointer = 0

        while 0 <= pointer < len(program):
            program_command = program[pointer]
            command, register, *value = program_command.split(" ")

            delta = getattr(self, command)(register, *value)
            if delta is not None:
                pointer += delta
            else:
                break


class DuetMachine(BaseMachine):
    def __init__(self, pid: int):
        super().__init__()
        self.waiting =  False
        self._pid = pid
        self._registers["p"] = pid
        self._queue = []
        self.send_count = 0
        self.pointer = 0

    def snd(self, register: str, target: Callable[[int], None]):
        self.send_count += 1
        target(self._registers[register])

        return 1

    def rcv(self, register: str):
        if self._queue:
            self._registers[register] = self._queue.pop(0)
            self.waiting = False

            return 1

        self.waiting = True
        return 0

    def queue(self, value: int):
        self._queue.append(value)

    def execute(self, program: list[str], receiver: Callable[[int], None]):
        if self.pointer < 0 or self.pointer >= len(program):
            self.waiting = True
            return

        command, register, *value = program[self.pointer].split(" ")

        if command == "snd":
            self.pointer += self.snd(register=register, target=receiver)
        else:
            self.pointer += getattr(self, command)(register, *value)


def main(filename: str):
    with open(filename) as f:
        program = [_.strip() for _ in f.readlines()]

    machine = SoloMachine()
    machine.run(program)
    print(f"The first non-zero value to be received is {machine.signal}.")

    machine_0 = DuetMachine(0)
    machine_1 = DuetMachine(1)

    while not (machine_0.waiting and machine_1.waiting):
        machine_0.execute(program=program, receiver=machine_1.queue)
        machine_1.execute(program=program, receiver=machine_0.queue)

    print(f"When both programs are in a deadlock program 1 has sen {machine_1.send_count} times.")


if __name__ == "__main__":
    main("input.txt")
