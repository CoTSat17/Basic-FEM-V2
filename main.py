import pygame
from menus import Menus




# pygame setup
pygame.init()
screen_x = 1280
screen_y = 720
screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()
running = True



#MENUS setup

menus = Menus(screen)
menus.new_menu("B", 100)



while running:
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



    menus.render_menus()


    pygame.display.flip()

    clock.tick(60)  

pygame.quit()