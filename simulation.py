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
        self.nb_turn:int = 0
        self.sim_log:List[str] = []
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
        self.nb_turn += 1
        turn_move = []
        terminal_output = []

        for key in self.size_of_conx:
            self.size_of_conx[key][0] = 0

        for drone in self.drones:
            if drone.pos >= len(drone.path) - 1:
                continue
            
            if drone.status > 0:
                drone.status -= 1
                continue

            current_zone = drone.path[drone.pos]
            next_zone = drone.path[drone.pos + 1]
            
            link_key = f"{current_zone}-{next_zone}"
            if not link_key in self.size_of_conx:
                link_key = f"{next_zone}-{current_zone}"
            
            curr_z_dr, max_z_dr = self.size_of_zone[next_zone]
            curr_c_d, max_c_d = self.size_of_conx[link_key] 

            zone_space =  curr_z_dr < max_z_dr
            link_space = curr_c_d < max_c_d
            if zone_space and link_space:
                self.size_of_zone[current_zone][0] -= 1
                self.size_of_zone[next_zone][0] += 1
                self.size_of_conx[link_key][0] += 1
                drone.pos += 1
                for zone in self.graph.data.hub:
                    if zone == next_zone:
                        if self.graph.data.hub[zone].type_zone == "restricted":
                            drone.status = 2
                turn_move.append({
                    "drone_id": drone.id,
                    "to_zone": next_zone
                })

                terminal_output.append(f"D{drone.id}-{next_zone}")
        if terminal_output:
            turn_str = (" ".join(terminal_output))
            print(f"turn: {self.nb_turn}")
            print(turn_str)
            self.sim_log.append(turn_str)
        
        return turn_move    
    
    
    def is_finished(self)-> bool:
        end = self.graph.data.end_hub.name
        return self.size_of_zone[end][0] == self.graph.data.nb_drones
                 
        
    
            
            
        
            
    