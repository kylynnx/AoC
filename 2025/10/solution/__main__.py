from machine_factory import MachineFactory


def main(filename: str):
    with open(filename) as f:
        machines = [MachineFactory.build(_.strip()) for _ in f.readlines()]

    optimal_lights_configuration = sum(_.lights_configuration_length for _ in machines)
    print(f"A total of {optimal_lights_configuration} button presses is needed to initialize all machines.")

    optimal_joltage_configuration = sum(_.joltages_configuration_length for _ in machines)
    print(f"It takes an additional {optimal_joltage_configuration} button presses to initialize the joltages.")


if __name__ == "__main__":
    main("../test.txt")
    main("../input.txt")
