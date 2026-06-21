import pygame

pygame.init()

s_width = 1500
s_height = 1500
screen = pygame.display.set_mode((s_width,s_height))

player = pygame.Rect((0,0,50,50))
run = True
while run:
    screen.fill((0,0,0))
    pygame.draw.rect(screen,(255,54,55), player)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] == True:
        player.move_ip(-1,0)
    if keys[pygame.K_RIGHT] == True:
        player.move_ip(1,0)
    if keys[pygame.K_UP] == True:
        player.move_ip(0,-1)
    if keys[pygame.K_DOWN] == True:
        player.move_ip(0,1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("clicked")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print("left")
        pygame.display.update()
pygame.quit()   