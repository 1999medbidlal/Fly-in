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
        self.name = pygame.display.set_caption("Fly-in")
        self.mode_scr = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.positions = {}

        # ➜ 2. هنا كنحسبو القيم الحقيقية إيلا كانت الداتا كاينا
        self.calculate_bounds()

    def load_image(self, path_img):
        bg = pygame.image.load(path_img).convert_alpha()
        rect = bg.get_rect()
        rect.center = (self.width // 2, self.height // 2)
        bg = pygame.transform.smoothscale(bg, (self.width, self.height))
        return bg

    def draw_screen(self, bg):
        rect = bg.get_rect()
        rect.center = (self.width // 2, self.height // 2)
        self.mode_scr.blit(bg, rect)

    #Bounding Box
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
        
        margin = 120
        map_width = self.width - 2 * margin
        map_height = self.height - 2 * margin
        for zone in all_nodes:
            norm_x = (zone.x - min_x) / (max_x - min_x + 1e-5)
            norm_y = (zone.y - min_y) / (max_y - min_y + 1e-5)
            screen_x = margin + norm_x * map_width
            screen_y = margin + norm_y * map_height
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
        pygame.draw.circle(self.screen.mode_scr, color, pos, 25)

    def draw_end_hub(self):
        color = get_color(self.data.end_hub.color_zone)
        pos = self.screen.screen_coords(self.data.end_hub.x,
                                        self.data.end_hub.y)
        pygame.draw.circle(self.screen.mode_scr, color, pos, 25)

    def draw_hub(self):
        for name, value in self.data.hub.items():
            color = get_color(value.color_zone)
            pos = self.screen.screen_coords(value.x, value.y)
            pygame.draw.circle(self.screen.mode_scr, color, pos, 15)


def redrawGame(screen, bg, zones):
    screen.draw_screen(bg)
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
    bg = screen.load_image("img/bg.png")
    screen.draw_screen(bg)
    zones = Zones_visu(data, screen)

    run = True
    while run:
        screen.clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        redrawGame(screen, bg, zones)


# class Drone:

#     def __init__(self,x, y, width, height):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height

#     def load_img(self, path_img):
#        img = pygame.image.load(path_img).convert_alpha()
#        img = pygame.transform.smoothscale(img, (self.width, self.height))
#        return img

#     def draw(self, screen, img):
#         pass
