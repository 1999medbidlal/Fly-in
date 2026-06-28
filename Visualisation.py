import pygame
from parce_data import Data


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
            pos1 = self.screen.screen_coords(res_zon1.x, res_zon1.y)
            pos2 = self.screen.screen_coords(res_zon2.x, res_zon2.y)
            pygame.draw.line(self.screen.mode_scr, self.color_conx, pos1, pos2,
                             3)


class Drones_visu(Connection_visu):

    def __init__(self, data, screen, path):
        super().__init__(data, screen)
        self.path = path
        self.img = pygame.image.load("img/drone.png")
        self.img = pygame.transform.scale(self.img, (60, 60))
        self.drones_list = []

        for i, (dr_name, path_names) in enumerate(self.path.items(), start=1):
            self.path_pixels = []
            for name in path_names:
                res = self.get_hub_by_name(name)
                d_x, d_y = self.screen.screen_coords(res.x, res.y)
                self.path_pixels.append((d_x, d_y))
            drone_info = {
                "name": dr_name,
                "path_pixels": self.path_pixels,
                "current_x": self.path_pixels[0][0],
                "current_y": self.path_pixels[0][1],
                "target": 1,
                "speed": 8,
                "delay": i * 30
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
                distance = (dx**2 + dy**2)**0.5
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
                pos_x = drone["current_x"] - img_width // 2
                pos_y = drone["current_y"] - img_height // 2
                self.screen.mode_scr.blit(self.img, (pos_x, pos_y))

    def reset(self) -> None:
        for drone in self.drones_list:
            drone["current_x"] = self.path_pixels[0][0]
            drone["current_y"] = self.path_pixels[0][1]
            drone["target"] = 1


def redrawGame(screen, zones, conx, drone):
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
        return pygame.Color("red")


def run(data, path):

    pygame.init()
    screen = Screen(data)
    screen.mode_scr
    screen.draw_screen()
    zones = Zones_visu(data, screen)
    conx = Connection_visu(data, screen)

    my_paths = {"drone1": path[0]}

    drone = Drones_visu(data, screen, my_paths)
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
