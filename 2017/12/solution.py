def main(filename: str):
    with open(filename) as f:
        connection_strings = [_.strip() for _ in f.readlines()]

    connections = {}
    for connection_string in connection_strings:
        pid, connected = connection_string.split(" <-> ")
        program = int(pid)
        connected_pids = [int(_) for _ in connected.split(", ")]
        connections[program] = [_ for _ in connected_pids if _ != program]

    connected_programs = get_all_connected_programs(connections=connections, root_id=0)
    connected_count = len(connected_programs)
    print(f"There are {connected_count} programs in the group with program 0.")

    programs = set(connections.keys()) - connected_programs
    groups = 1
    while programs:
        program = programs.pop()
        connected = get_all_connected_programs(connections=connections, root_id=program)
        groups += 1
        programs -= connected

    print(f"There are {groups} groups of programs in total.")


def get_all_connected_programs(connections: dict, root_id: int) -> set[int]:
    connected_programs = set()
    evaluated_ids = set()

    queue = [root_id]
    while queue:
        current_id = queue.pop(0)

        if current_id in evaluated_ids:
            continue
        else:
            evaluated_ids.add(current_id)

        connected_programs.add(current_id)
        for program in connections[current_id]:
            connected_programs.add(program)
            if program not in evaluated_ids:
                queue.append(program)

    return connected_programs


if __name__ == "__main__":
    main("test.txt")
    main("input.txt")
