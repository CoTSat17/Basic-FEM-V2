import pygame
from menus import Menus




# pygame setup
pygame.init()
screen_x = 1280
screen_y = 720
screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()
running = True






#__ MENUS setup __

menus = Menus(screen)
bot_menu = menus.new_menu("B", 100, )
## Buttons setup
button_test = bot_menu.create_button((10,10),(80,40),"TEST")
button_test.change_active()



while running:
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")
    


    menus.render_menus()


    pygame.display.flip()

    clock.tick(60)  

pygame.quit()