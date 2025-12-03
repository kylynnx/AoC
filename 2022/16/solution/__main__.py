from valve_system import ValveSystem


def main(filename: str):
    valve_system = ValveSystem(filename)
    # max_flow = valve_system.get_max_flow()
    # print(max_flow)
    max_flow_with_elephant_support = valve_system.get_max_flow_with_elephant_support()
    print(max_flow_with_elephant_support)


if __name__ == '__main__':
    main('../input.txt')
