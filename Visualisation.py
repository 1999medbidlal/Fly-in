import pygame
from parce_data import Parce_Data
import sys


class Screen:

    def __init__(self,
                 data: Parce_Data,
                 s_width: int = 1500,
                 s_height: int = 900) -> None:
        self.width = s_width
        self.height = s_height
        self.data = data
        self.color = get_color("Beige")
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
        
        margin_x = 150
        margin_y = 250
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

    def draw_start_hub(self):
        color = get_color(self.data.start_hub.color_zone)
        pos = self.screen.screen_coords(self.data.start_hub.x,
                                        self.data.start_hub.y)
        size = 50
        rect_start = (pos[0] - size//2, pos[1] - size//2, size, size)
        pygame.draw.rect(self.screen.mode_scr, color, rect_start)

    def draw_end_hub(self):
        color = get_color(self.data.end_hub.color_zone)
        pos = self.screen.screen_coords(self.data.end_hub.x,
                                        self.data.end_hub.y)
        size = 50
        rect_end = (pos[0] - size//2, pos[1] - size//2, size, size)
        pygame.draw.rect(self.screen.mode_scr, color,rect_end)

    def draw_hub(self):
        for _, value in self.data.hub.items():
            color = get_color(value.color_zone)
            pos = self.screen.screen_coords(value.x, value.y)
            pygame.draw.circle(self.screen.mode_scr, color,pos,30)

class Connection(Zones_visu):
    
    def __init__(self, data, screen):
        self.color_conx =  get_color("RED")
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
             

def redrawGame(screen, zones,conx):
    screen.draw_screen()
    conx.draw_connection()
    zones.draw_start_hub()
    zones.draw_end_hub()
    zones.draw_hub()
    pygame.display.update()


def get_color(name_color):
    try:
        color = pygame.Color(name_color)
        return color
    except ValueError:
        raise ValueError("Color name is invalid")


def run(data):

    pygame.init()  # init pygame
    screen = Screen(data)
    screen.mode_scr
    screen.draw_screen()
    zones = Zones_visu(data, screen)
    conx = Connection(data, screen)
    
    run = True
    while run:
        screen.clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            quit()
        redrawGame(screen, zones, conx)

