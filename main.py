import pygame
from menus import Menus
from drawing import Drawing


def mouse_button_event():
    """
    Used to handle mouse clicks
    ::RETURN::
        -True if the main screen was clicked
    """

    # LEFT BUTTON
    if pygame.mouse.get_pressed(3)[0]: 
        if not menus.click_event(): # False if a menu was not clicked
            #Only executed if a menu wan't clicked
            return True



# pygame setup
pygame.init()
screen_x = 1280
screen_y = 720
screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()
running = True


click_event = True


#__ MENUS setup __

menus = Menus(screen)
bot_menu = menus.new_menu("B", 100)

## Buttons setup
button_drawing = bot_menu.create_button((10,10),(80,40),"DRAW")


#__ DRAWING Setup __
drawings = Drawing(screen)



while running:

    # ___ EVENTS ___
    mouse_click = False # Checks if in this frame was a "mousebuttondown" event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # MOUSE CLICK
        if event.type == pygame.MOUSEBUTTONDOWN: #Second condition to get only 1 event per click
            mouse_click = mouse_button_event()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                #Deactivate all menu buttons and go to default state
                menus.reset_all_buttons()
        



    screen.fill("white")
    


    drawings.flip(mouse_click, button_drawing.active)
    menus.render_menus()



    pygame.display.flip()

    clock.tick(60)  

pygame.quit()