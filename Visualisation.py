import pygame
from parce_data import Data



class Screen:

    def __init__(self,
                 data: Data,
                 s_width: int = 1800,
                 s_height: int = 900) -> None:
        self.width = s_width
        self.height = s_height
        self.data = data
        self.color = get_color("Teal")
        self.name = pygame.display.set_caption("Fly-in")
        self.mode_scr = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.positions = {}
        self.calculate_bounds()
    
    def draw_screen(self):
        self.mode_scr.fill(self.color)

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
        min_y, max_y =  min(all_y), max(all_y)
        
        margin_x = 50
        margin_y = 50
        map_width = self.width - 2 * margin_x
        map_height = self.height - 2 * margin_y
        for zone in all_nodes:
            norm_x = (zone.x - min_x) / (max_x - min_x + 1e-5)
            norm_y = (zone.y - min_y) / (max_y - min_y + 1e-5)
            screen_x = margin_x + norm_x * map_width
            screen_y = margin_y + norm_y * map_height
            self.positions[(zone.x,zone.y)] = (int(screen_x),int(screen_y))

    def screen_coords(self, x, y):
        if (x, y) in self.positions:
            return self.positions[(x,y)]
 


class Zones_visu:

    def __init__(self, data, screen):
        self.data = data
        self.screen = screen

    def draw_zones(self):
        if self.data.start_hub:
            color = get_color(self.data.start_hub.color_zone)
            pos = self.screen.screen_coords(self.data.start_hub.x,
                                            self.data.start_hub.y)
            size = 60
            rect_start = (pos[0] - size//2, pos[1] - size//2, size, size)
            pygame.draw.rect(self.screen.mode_scr, color, rect_start)

        if self.data.end_hub:
            color = get_color(self.data.end_hub.color_zone)
            pos = self.screen.screen_coords(self.data.end_hub.x,
                                            self.data.end_hub.y)
            size = 60
            rect_end = (pos[0] - size//2, pos[1] - size//2, size, size)
            pygame.draw.rect(self.screen.mode_scr, color,rect_end)

        for value in self.data.hub.values():
            color = get_color(value.color_zone)
            pos = self.screen.screen_coords(value.x, value.y)
            pygame.draw.circle(self.screen.mode_scr, color,pos,30)
    
    

class Connection_visu(Zones_visu):
    
    def __init__(self, data, screen):
        self.color_conx =  get_color("Mustard")
        super().__init__(data, screen)
    
    def get_hub_by_name(self, name):
        if name == self.data.start_hub.name:
            return self.data.start_hub
        if name == self.data.end_hub.name:
            return self.data.end_hub
        if name in self.data.hub:
            return self.data.hub[name]
             
    def draw_connection(self):
        for c in self.data.connections:
            res_zon1 = self.get_hub_by_name(c.zone1)
            res_zon2 = self.get_hub_by_name(c.zone2)
            pos1 = self.screen.screen_coords(res_zon1.x,res_zon1.y)
            pos2 = self.screen.screen_coords(res_zon2.x, res_zon2.y)
            pygame.draw.line(self.screen.mode_scr,self.color_conx, pos1, pos2, 3)

class Drones_visu(Connection_visu):
    def __init__(self, data, screen, path):
        super().__init__(data, screen)
        self.path = path
        self.img = pygame.image.load("img/drone.png")
        self.img = pygame.transform.scale(self.img, (60, 60))
        self.drones_list = []
 
        for i, (dr_name, path_names) in enumerate (self.path.items(), start= 1):
            self.path_pixels = []
            for name in path_names:
                res = self.get_hub_by_name(name)
                d_x, d_y=  self.screen.screen_coords(res.x, res.y)
                self.path_pixels.append((d_x,d_y))
            drone_info = {
                "name":dr_name,
                "path_pixels":self.path_pixels,
                "current_x": self.path_pixels[0][0],
                "current_y": self.path_pixels[0][1],
                "target": 1,
                "speed": 4,
                "delay": i * 40   
            }
            self.drones_list.append(drone_info)
    def move_drones(self):
        for drone in self.drones_list:
            if drone["delay"] > 0:
                drone["delay"] -= 1
                continue

            if drone["target"] < len(drone["path_pixels"]):
                target_x, target_y = drone["path_pixels"][drone["target"]]
                dx = target_x - drone["current_x"]
                dy = target_y - drone["current_y"]
                distance = (dx**2 + dy**2)** 0.5
                if distance <= drone["speed"]:
                    drone["current_x"], drone["current_y"] = target_x, target_y
                    drone["target"] += 1
                else:
                    drone["current_x"] += (dx / distance) * drone["speed"]
                    drone["current_y"] += (dy / distance) * drone["speed"]
                  
    
    def draw_drone(self) -> None:
        img_width = self.img.get_width()
        img_height = self.img.get_height()
        for drone in self.drones_list:
            if drone["delay"] == 0:
                pos_x = drone["current_x"]- img_width // 2
                pos_y = drone["current_y"] - img_height // 2
                self.screen.mode_scr.blit(self.img, (pos_x, pos_y))
        
    def reset(self) -> None:
        for drone in self.drones_list:
            drone["current_x"] = self.path_pixels[0][0]
            drone["current_y"] = self.path_pixels[0][1]
            drone["target"] = 1
    
    

def redrawGame(screen, zones,conx,drone):
    screen.draw_screen()
    conx.draw_connection()
    zones.draw_zones()
    drone.draw_drone()
   
    pygame.display.update()


def get_color(name_color):
    try:
        color = pygame.Color(name_color)
        return color
    except ValueError:
        return pygame.Color("gray")


def run(data, path):

    pygame.init()
    screen = Screen(data)
    screen.mode_scr
    screen.draw_screen()
    zones = Zones_visu(data, screen)
    conx = Connection_visu(data, screen)
    
    my_paths = {
        "drone1": path
    }
    
    drone = Drones_visu(data, screen,my_paths)
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
            drone.move_drones()
        redrawGame(screen, zones, conx, drone)

