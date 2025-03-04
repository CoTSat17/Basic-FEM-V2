import pygame


class Menus():
        def __init__(self, screen:pygame.Surface):
                self.menus = []
                self.screen = screen
                self.screen_size = (screen.get_width(), screen.get_height())

        def new_menu(self, orientation:str, size:int):
                """
                Adds a new menu\n
                ::INPUT:: \n
                orientation: "T" top; "R" right; "B" bot; "L" left\n
                size: height of the menu
                """
                self.menus.append(Menu(orientation, size, self.screen_size))

        def render_menus(self):
                """
                Renders the menu to the screen
                """
                for menu in self.menus:
                        self.screen.blit(menu, menu.position)


        def __update_menus(self):
                """
                Updates the menus position and size\n
                Depends on the menu orientation
                """
                for menu in self.menus:
                        menu.update_menu(self)


class Menu(pygame.Surface):
        def __init__(self, orientation:str, size:int, screen_size):
                
                self.orientation = orientation
                self.size = size

                self.position = ()
                self.dimmension = ()
                self.update_menu(screen_size) 

                super().__init__(self.dimmension) #Generates the Surface

                self.fill("white")




        def update_menu(self, screen_size:tuple[int,int]):
                """
                Updates the menu in dimmension and position based on orientation
                """
                # Update position
                ## The dicitionary creates the different posibilities and the corresponding to the orientation is selected
                position_options = {"T": (0,0), 
                                    "R": (screen_size[0] - self.size), 
                                    "B": (0, screen_size[1]- self.size),
                                    "L": (0,0)}
                self.position = position_options[self.orientation]
                # Update dimmension
                ## The dicitionary creates the different posibilities and the corresponding to the orientation is selected
                dimmension_option = {"T": (screen_size[0], self.size),
                                     "B": (screen_size[0], self.size),
                                     "R": (self.size, screen_size[1]),
                                     "L": (self.size, screen_size[1])}
                self.dimmension = dimmension_option[self.orientation]
