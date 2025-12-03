import re
from typing import List


class Valve:
    def __init__(self, valve_config: str):
        if 'leads' in valve_config:
            valve_config = valve_config.replace('leads', 'lead').replace('valve', 'valves').replace('tunnel', 'tunnels')

        config_match = re.match(
            r'Valve ([A-Z]+) has flow rate=(\d+); tunnels lead to valves? ([A-Z,\s]+)+$', valve_config
        )

        self._name = config_match.group(1)
        self._flow_rate = -int(config_match.group(2))
        self._tunnels = config_match.group(3).split(', ')

    @property
    def name(self) -> str:
        return self._name

    @property
    def flow_rate(self) -> int:
        return self._flow_rate

    @property
    def tunnels(self) -> List[str]:
        return self._tunnels
