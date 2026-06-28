from parce_data import Data
from typing import Dict, List


class Graph:

    def __init__(self, data: Data) -> None:
        self.data = data
        self.neighbors: Dict[str, List] = {zone: [] for zone in self.data.hub}
        self.get_neighbor()
        self.start = self.data.start_hub
        self.end = self.data.end_hub
        self.key_cost = {
                "normal": 1.0,
                "blocked": 1.0,
                "restricted": 2.0,
                "priority": 0.9
            }
        self.cost = {
                key: self.key_cost[value.type_zone]
                for key, value in self.data.hub.items()
            }

    def get_neighbor(self):
        for conx in self.data.connections:
            z1, z2, max_link = conx.zone1, conx.zone2, conx.max_link
            zone1 = self.data.hub[z1]
            zone2 = self.data.hub[z2]
            self.neighbors[z1].append((zone2, max_link))
            self.neighbors[z2].append((zone1, max_link))

    def algo_dijkstra(self) -> List[str]:
        if self.start is None or self.end is None:
            raise ValueError("zone None")

        weight: Dict[str, float] = {
            zone: float("inf")
            for zone in self.data.hub.keys()
        }
        res: Dict[str, str] = {}
        weight[self.start.name] = 0
        queue = []
        queue.append(self.start)
        while queue:

            current_zone = min(queue, key=lambda zone: weight[zone.name])
            if current_zone.name == self.end.name:
                break
            queue.remove(current_zone)
            neighbor = [zone[0] for zone in self.neighbors[current_zone.name]]
            for n in neighbor:

                if n.type_zone == "blocked":
                    continue
                new_weight = weight[current_zone.name] + self.cost[n.name]
                if new_weight < weight[n.name]:
                    weight[n.name] = new_weight
                    queue.append(n)
                    res[n.name] = current_zone.name
        if weight[self.data.end_hub.name] == float("inf"):
            raise ValueError("not path found")
        path = []
        zone: str = self.end.name
        path.append(zone)
        while True:
            path.append(res[zone])
            zone = res[zone]
            if zone == self.start.name:
                return path[::-1]

    def refind_path(self):
        all_path = []
        while True:
            path = self.algo_dijkstra()
            if path in all_path:
                break
            all_path.append(path)
            for name_zone in path:
                self.cost[name_zone] += 5
            
        return all_path