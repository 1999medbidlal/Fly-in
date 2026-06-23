import pygame

move_right = [pygame.image.load("hero/R1.png"), pygame.image.load("hero/R2.png"), pygame.image.load("hero/R3.png"), pygame.image.load("hero/R4.png"), pygame.image.load("hero/R5.png"), pygame.image.load("hero/R6.png"), pygame.image.load("hero/R7.png"), pygame.image.load("hero/R8.png"), pygame.image.load("hero/R9.png")]
move_left = [pygame.image.load("hero/L1.png"), pygame.image.load("hero/L2.png"), pygame.image.load("hero/L3.png"), pygame.image.load("hero/L4.png"), pygame.image.load("hero/L5.png"), pygame.image.load("hero/L6.png"), pygame.image.load("hero/L7.png"), pygame.image.load("hero/L8.png"), pygame.image.load("hero/L9.png")]
# left = False
# right = False
# moves =  0
#dron = pygame.transform.rotate(dron, -60)


class Screen:

    def __init__(self, name, s_width, s_height):
        self.width = s_width
        self.height = s_height
        self.name = pygame.display.set_caption(name)

    def set_mode(self) -> None:
        scr = pygame.display.set_mode(
            (s_width, s_height))  # demionsion of screen
        return scr

    def load_image(self, path_img):
        bg = pygame.image.load(path_img).convert_alpha()
        rect = bg.get_rect()
        rect.center = (self.width // 2, self.height // 2)
        bg = pygame.transform.smoothscale(bg, (self.width, self.height))
        return bg


class Herro:

    def __init__(self, color, x, y, width, height):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.step = 5
        self.speed = 12
        self.isjump = False
        self.ground_y = y
        self.left = False
        self.right = False
        self.moves = 0

    def load_img(self, path_img):
       img = pygame.image.load(path_img).convert_alpha()
       img = pygame.transform.smoothscale(bg, (self.width, self.height))
       return img
    
    def draw(self, screen, img):
        if self.left:
            screen.blit(move_left[self.moves // 2], (self.x, self.y))
            self.moves += 1
            if self.moves == 18:
                self.moves = 0
        elif self.right:
            screen.blit(move_right[self.moves // 2], (self.x, self.y))
            self.moves += 1
            if self.moves == 18:
                self.moves = 0
        else:
            screen.blit(img, (self.x, self.y))

def get_color(name_color):
    try:
        color = pygame.Color(name_color)
        return color
    except ValueError:
        raise ValueError("Color name is invalid")
       



def redrawGame(mode_scrn, bg_img, player,player_img):
    global moves
    #khlifiya
    #screen.fill(BLUE)
    #bg images
    rect = bg_img.get_rect()
    rect.center = (s_width // 2, s_height // 2)
    mode_scrn.blit(bg_img, rect)
    player.draw(mode_scr, player_img)
    pygame.display.update()





if __name__ == "__main__":
    try:
        clock = pygame.time.Clock()
        s_width = 1024
        s_height = 700
        s_name = "Fly-in"
        pygame.init()  # init pygame
        screen = Screen(s_name, s_width, s_height)
        mode_scr = screen.set_mode()
        bg = screen.load_image("bgs.jpg")

        #player
        n_color = "blue"
        x = 50
        y = 280
        p_wdith = 50
        p_height = 50
        color = get_color(n_color)
        p1 = Herro(color, x, y, p_wdith, p_height)
        img_p1 = p1.load_img("drone.png")
        redrawGame(mode_scr, bg,p1,img_p1)
        while True:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

        # moves =  0
        # x = 50
        # y = 280
        # p_wdith = 50
        # p_height = 50 #IRTIFA3
        # step = 5 #khotowat

        # #9afz
        # speed = 12
        # isjump = False
        # ground_y = y

        # name of programme

        # run = True
        # while run:
        #     clock.tick(30)

        #     for event in pygame.event.get():
        #         #quit programme
        #         if event.type == pygame.QUIT:
        #             quit()

        #     #move player
        #     #-> isti9bal jami3 keys
        #     keys = pygame.key.get_pressed()
        #     #quit py
        #     if keys[pygame.K_q]:
        #         quit()
        #     #khotowat
        #     if keys[pygame.K_LEFT] and x - step >= 0: #<-
        #         x -= step
        #         left = True
        #         right = False
        #     elif keys[pygame.K_RIGHT] and x + p_wdith + step <= s_width:
        #         x += step
        #         left = False
        #         right = True
        #     else:
        #         right = False
        #         left = False
        #     if not isjump:
        #         if keys[pygame.K_UP] and y - step >= 0:
        #             y -= step
        #             ground_y = y
        #         if keys[pygame.K_DOWN] and y + p_height + step <= s_height:
        #             y += step
        #             ground_y = y
        #         if keys[pygame.K_SPACE]:
        #             isjump = True
        #     else:
        #         if speed >= -12:
        #             nega = 1
        #             if speed < 0:
        #                 nega = -1
        #             y -= (speed ** 2) * 0.25 * nega
        #             speed -= 1
        #         else:
        #             isjump = False
        #             speed = 12
        #             ground_y = y

        #         if y < 0:
        #             y = 0

        #         if y + p_height > s_height:
        #             y = s_height - p_height + step
        #     read_draw()
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")

# while True:
#     pygame.time.delay(100)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             quit()
