from Algo_dijkstra import Graph
from typing import List, Dict
class Drone:
    def __init__(self,dr_id,path:List[str]):
        self.id = dr_id
        self.path = path
        self.pos = 0
        self.status = 0

class Sim:
    def __init__(self, graph:Graph):
        self.graph = graph
        self.paths:List[List[str]] = self.graph.refind_path()
        self.drones:List[Drone] = []
        self.size_of_zone:Dict[str,List[int]] = {}
        self.size_of_conx:Dict[str,List[int]] = {}
        self.init_drones()
        self.init_zone()
        self.init_conx()
        
    def init_drones(self):
        for i in range(self.graph.data.nb_drones):
            drone = Drone(i + 1, self.paths[(i % len(self.paths))])
            self.drones.append(drone)
    
    def init_zone(self):
        for zone in self.graph.data.hub.values():
            max_drones =  zone.max_drones
            self.size_of_zone[zone.name] = [0, max_drones]
        max_drone = self.graph.data.start_hub.max_drones
        self.size_of_zone[self.graph.data.start_hub.name][0] = max_drone
    
    def init_conx(self):
        for conx in self.graph.data.connections:
            max_link = conx.max_link
            zone_1 = conx.zone1
            zone_2 =  conx.zone2 
            self.size_of_conx[f"{zone_1}-{zone_2}"] = [0, max_link]
    
    def run_simulation(self):
        end = self.graph.data.end_hub.name
        turn_output:List[str] = []
        nb_turn:int = 0
        while True:
            for drone in self.drones:
                pass
            if self.size_of_zone[end][0] == self.size_of_zone[end][1]:
                break 
        
    
            
            
        
            
    