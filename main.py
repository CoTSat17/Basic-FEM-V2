import pygame
from menus import Menus




# pygame setup
pygame.init()
screen_x = 1280
screen_y = 720
screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()
running = True


click_event = None


#__ MENUS setup __

menus = Menus(screen)
bot_menu = menus.new_menu("B", 100)
top_menu = menus.new_menu("T", 100)

## Buttons setup
button_test = bot_menu.create_button((10,10),(80,40),"TEST")
button_test.change_active()



while running:

    mouse_click = False # Checks if in this frame was a "mousebuttondown" event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse click events
        if event.type == pygame.MOUSEBUTTONDOWN and click_event == None: #Second condition to get only 1 event per click
            click_event = event
            mouse_click = True

    if not mouse_click:
        click_event = None

    
    screen.fill("white")
    


    menus.flip(click_event)


    pygame.display.flip()

    clock.tick(60)  

pygame.quit()