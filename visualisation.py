import pygame
from typing import Dict, List
from parce_data import Data
from simulation import Sim


class Screen:

    def __init__(self,
                 data: Data,
                 s_width: int = 1600,
                 s_height: int = 850) -> None:
        self.width = s_width
        self.height = s_height
        self.data = data
        self.name = pygame.display.set_caption("Fly-in")
        self.mode_scr = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.positions = {}
        self.calculate_bounds()
        self.bg_img = pygame.image.load("img/bg.png")
        self.bg_img = pygame.transform.smoothscale(
            self.bg_img, (self.width, self.height + 180))

    def draw_screen(self):
        self.mode_scr.blit(self.bg_img, (0, 0))

    def calculate_bounds(self):
        all_nodes = []
        if self.data.start_hub:
            all_nodes.append(self.data.start_hub)
        if self.data.end_hub:
            all_nodes.append(self.data.end_hub)
        for zone in self.data.hub.values():
            all_nodes.append(zone)
        all_x = [z.x for z in all_nodes]
        all_y = [z.y for z in all_nodes]
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)

        margin_x = 50
        margin_y = 50
        map_width = self.width - 2 * margin_x
        map_height = self.height - 2 * margin_y
        for zone in all_nodes:
            norm_x = (zone.x - min_x) / (max_x - min_x + 1e-5)
            norm_y = (zone.y - min_y) / (max_y - min_y + 1e-5)
            screen_x = margin_x + norm_x * map_width
            screen_y = margin_y + norm_y * map_height
            self.positions[(zone.x, zone.y)] = (int(screen_x), int(screen_y))

    def screen_coords(self, x, y):
        if (x, y) in self.positions:
            return self.positions[(x, y)]


class Zones_visu:

    def __init__(self, data, screen):
        self.data: Data = data
        self.screen: Screen = screen

    def draw_zones(self):
        if self.data.start_hub:
            color = get_color(self.data.start_hub.color_zone)
            pos = self.screen.screen_coords(self.data.start_hub.x,
                                            self.data.start_hub.y)
            size = 73
            rect_start = (pos[0] - size // 2, pos[1] - size // 2, size, size)
            pygame.draw.rect(self.screen.mode_scr, color, rect_start)
            start_img = pygame.image.load("img/start.png")
            size_img = 93
            start_img = pygame.transform.smoothscale(start_img,
                                                     (size_img, size_img))
            pos_start = (pos[0] - size_img // 2, pos[1] - size_img // 2)
            self.screen.mode_scr.blit(start_img, pos_start)

        if self.data.end_hub:
            color = get_color(self.data.end_hub.color_zone)
            pos = self.screen.screen_coords(self.data.end_hub.x,
                                            self.data.end_hub.y)
            size = 57
            rect_end = (pos[0] - size // 2, pos[1] - size + 10 // 2, size,
                        size + 50)
            pygame.draw.rect(self.screen.mode_scr, color, rect_end)
            end_img = pygame.image.load("img/exit.png").convert_alpha()
            size_end = 93
            end_img = pygame.transform.smoothscale(end_img,
                                                   (size_end, size_end))
            pos_end = (pos[0] - size_img // 2, pos[1] - size_img // 2)
            self.screen.mode_scr.blit(end_img, pos_end)

        hub_img = pygame.image.load("img/target.png").convert_alpha()
        for key, value in self.data.hub.items():
            if self.data.start_hub.name == key:
                continue
            if self.data.end_hub.name == key:
                continue
            color = get_color(value.color_zone)
            pos = self.screen.screen_coords(value.x, value.y)
            pygame.draw.circle(self.screen.mode_scr, color, pos, 30)
            size = 60
            hub_img = pygame.transform.smoothscale(hub_img, (size, size))
            self.screen.mode_scr.blit(hub_img,
                                      (pos[0] - size // 2, pos[1] - size // 2))


class Connection_visu(Zones_visu):

    def __init__(self, data, screen):
        self.color_conx = get_color("gray")
        super().__init__(data, screen)

    def draw_connection(self):
        for c in self.data.connections:
            res_zon1 = self.data.hub[c.zone1]
            res_zon2 = self.data.hub[c.zone2]
            pos1 = self.screen.screen_coords(res_zon1.x, res_zon1.y)
            pos2 = self.screen.screen_coords(res_zon2.x, res_zon2.y)
            pygame.draw.line(self.screen.mode_scr, self.color_conx, pos1, pos2,
                             3)


class Drones_visu(Connection_visu):

    def __init__(self, data: Data, screen: Screen, sim: Sim):
        super().__init__(data, screen)
        self.sim = sim
        self.screen: Screen = screen
        self.img = pygame.image.load("img/drone.png")
        self.img = pygame.transform.scale(self.img, (60, 60))
        self.drone_positions = {}
        self.nb_turn = 0

        for drone in self.sim.drones:
            start_zone = drone.path[drone.pos]
            res = self.data.hub[start_zone]
            d_x, d_y = self.screen.screen_coords(res.x, res.y)
            self.drone_positions[drone.id] = {
                "current_x": d_x,
                "current_y": d_y,
                "target_x": d_x,
                "target_y": d_y,
                "is_move":False,
                "steps": 10,
            }   
    def move_drones(self, res:List[Dict]):
        self.nb_turn = self.sim.nb_turn 

        for drone in res:
            dr_id = drone["drone_id"]
            dr_from = drone["current_zone"]
            d_current = self.data.hub[dr_from]
            f_x, f_y = self.screen.screen_coords(d_current.x, d_current.y) 
            dr_target =  drone["to_zone"]
            d_targt = self.data.hub[dr_target]    
            t_x, t_y = self.screen.screen_coords(d_targt.x, d_targt.y)
            if dr_id in self.drone_positions:
                self.drone_positions[dr_id]["current_x"] = f_x 
                self.drone_positions[dr_id]["current_y"] = f_y  
                self.drone_positions[dr_id]["target_x"] = t_x 
                self.drone_positions[dr_id]["target_y"] = t_y
                self.drone_positions[dr_id]["is_move"]  = True
                
    def animation_drone(self):
        all_move =  False
        for drone in self.drone_positions.values():
            if drone["is_move"]:
                dx = drone["target_x"] - drone["current_x"]
                dy = drone["target_y"] - drone["current_y"]
                distance = (dx**2 + dy**2)**0.5
                if distance <= drone["steps"]:
                    drone["current_x"] = drone["target_x"] 
                    drone["current_y"] = drone["target_y"]
                    drone["is_move"] = False
                else:
                    drone["current_x"] += (dx / distance) * drone["steps"]
                    drone["current_y"] += (dy / distance) * drone["steps"]
                    all_move = True
        return all_move              

    def draw_drone(self) -> None:
        img_width = self.img.get_width()
        img_height = self.img.get_height()
        for drone in self.drone_positions.values():
                pos_x = drone["current_x"] - img_width // 2
                pos_y = drone["current_y"] - img_height // 2
                self.screen.mode_scr.blit(self.img, (pos_x, pos_y))

    def display_turn(self):
        font = pygame.font.SysFont(None, 30)
        text = font.render(f"NUMBER OF TURNS: {self.nb_turn}",True, get_color("black"))
        self.screen.mode_scr.blit(text, (1300, 50))
    
    def reset(self) -> None:
            start_zone = self.data.start_hub
            d_x, d_y = self.screen.screen_coords(start_zone.x, start_zone.y)
            for drone in self.drone_positions.values():
                drone["current_x"] =  d_x
                drone["current_y"] =  d_y
                drone["target_x"] = d_x
                drone["target_y"] = d_y
                drone["is_move"] = False
            self.nb_turn = 0
            self.sim.size_of_zone[self.data.end_hub.name][0] = 0
                
                


def redrawGame(screen, zones, conx, drone):
    screen.draw_screen()
    conx.draw_connection()
    zones.draw_zones()
    drone.draw_drone()
    drone.display_turn()

    pygame.display.update()


def get_color(name_color):
    try:
        color = pygame.Color(name_color)
        return color
    except ValueError:
        return pygame.Color("red")


def run(data, sim):

    pygame.init()
    screen = Screen(data)
    screen.mode_scr
    screen.draw_screen()
    zones = Zones_visu(data, screen)
    conx = Connection_visu(data, screen)

    drone = Drones_visu(data, screen, sim)
    pause = False

    while True:
        screen.clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == 32:
                    pause = not pause
                elif event.key == pygame.K_r:
                    drone.reset()
                elif event.key == pygame.K_q:
                    quit()

        if not pause:

                if not sim.is_finished():
                    is_moving = drone.animation_drone()
                    if not is_moving:
                        res = drone.sim.run_simulation()
                        drone.move_drones(res)
                        print(is_moving)
                    else:
                        drone.animation_drone()
                    
                
        redrawGame(screen, zones, conx, drone)
