import pygame

def coord_inside_surf(coord:tuple[int,int], surf_position:tuple[int,int], surf_size:tuple[int,int])-> bool:
        """
        Checks if a coord is inside a surf\n
        ::INPUT::
                -Coord: coordenates to be checked
                -Surf_position: Position on the top left of the surface
                -Surf_size: Size of the surface
        ::OUTPUT::
                -True: if inside
                -False: if outside
        """
        return 0 < coord[0] - surf_position[0] <  surf_size[0] and  0 < coord[1] - surf_position[1] <  surf_size[1]

        


pygame.font.init()
font_normal = pygame.font.SysFont("calibri", 20)
font_bold   = pygame.font.SysFont("calibri", 20, True)

class Menus():
        def __init__(self, screen:pygame.Surface):
                self.menus = []
                self.screen = screen
                self.screen_size = (screen.get_width(), screen.get_height())


        def new_menu(self, orientation:str, size:int)->"Menu":
                """
                Adds a new menu\n
                ::INPUT:: \n
                orientation: "T" top; "R" right; "B" bot; "L" left\n
                size: height of the menu\n
                ::OUTPUT:: \n
                Returns the created Menu instance
                """
                new_menu = Menu(orientation, size, self.screen_size)
                self.menus.append(new_menu)
                return new_menu


        def flip(self, event:pygame.event.Event):
                """
                Executes all needed functions for each frame\n
                \t -Detects button click\n
                \t -Renders menus and buttons\n
                ::INPUT::
                \t -Event: Clicking event
                """
                if event != None: # Checks if a "mousbuttonevent" occurred this frame
                        self.__click_event()
                self.__render_menus()


        def __click_event(self):
                """
                Handles the click event in the menus\n
                ::INPUT::
                        -Event: Clicking event

                ::OUTPUT::
                        -If click outside menus -> "None"
                """
                #Click Event
                clicked_menu = ""
                click_position = pygame.mouse.get_pos()
                for menu in self.menus:
                        #Check if its inside a menu
                        if  coord_inside_surf(click_position, menu.position, menu.dimmension):
                                clicked_menu = menu
                                break
                if clicked_menu == "": #If no menu was reached
                        return None


                for button in clicked_menu.buttons:
                        # The coord of the button are relative to the menu so must be adjusted
                        relative_click_position = (click_position[0] -menu.position[0], click_position[1] -menu.position[1])
                        if coord_inside_surf(relative_click_position, button.position, button.size):
                                button.change_active()
                        


        def __render_menus(self):
                """
                Renders the menu to the screen and its buttons
                """
                for menu in self.menus:
                        #Render the menu
                        self.screen.blit(menu, menu.position)
                        #Render the buttons
                        for button in menu.buttons:
                                button.blit(button.text_surf, button.text_position)
                                menu.blit(button, button.position)


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
                self.buttons = [] #List that contains the buttons in the menu

                self.position = ()
                self.dimmension = () 
                self.update_menu(screen_size) 

                super().__init__(self.dimmension) #Generates the Surface

                self.fill("gray")




        def update_menu(self, screen_size:tuple[int,int]):
                """
                Updates the menu:
                        Position
                        Dimmension
                """
                # __Update position__
                ## The dicitionary creates the different posibilities and the corresponding to the orientation is selected
                position_options = {"T": (0,0), 
                                    "R": (screen_size[0] - self.size, 0), 
                                    "B": (0, screen_size[1]- self.size),
                                    "L": (0,0)}
                self.position = position_options[self.orientation]

                # __Update dimmension__
                ## The dicitionary creates the different posibilities and the corresponding to the orientation is selected
                dimmension_option = {"T": (screen_size[0], self.size),
                                     "B": (screen_size[0], self.size),
                                     "R": (self.size, screen_size[1]),
                                     "L": (self.size, screen_size[1])}
                self.dimmension = dimmension_option[self.orientation]

                


        def create_button(self, position: tuple[int,int], size: tuple[int,int], text:str)-> "Button":
                """
                Creates a button in the Menu.\n
                ::INPUT::\n
                Position: Position of the button, relative to the surface\n
                Size: Size of the button\n
                Text: Text to be displayed in the button
                """
                new_button = Button(position, size, text)
                self.buttons.append(new_button)
                return new_button



# _________ BUTTONS _________

class Button(pygame.Surface):
        def __init__(self, position: tuple[int,int], size: tuple[int,int], text:str):
                """
                Generates a new button\n
                ::INPUT::\n
                Position: Position of the button, relative to the surface\n
                Size: Size of the button\n
                Text: Text to be displayed in the button
                """
                self.position = position
                self.size = size
                self.text = text
                self.__active = False

                #Text
                self.text_surf = font_normal.render(self.text, 0, "black")
                self.text_position = ( (self.size[0] - self.text_surf.get_width())/2 , (self.size[1] - self.text_surf.get_height())/2 )
                
                super().__init__(self.size)
                self.fill("dark gray")

        
        def change_active(self):
                """
                Changes the button from active to inactive or inverse\n
                Also changes the button colour.
                """
                if self.__active:       #Changes to inactive
                        self.__active = False
                        self.fill("dark gray")
                        self.text_surf = font_normal.render(self.text, 0, "black")
                else:                   #Changes to active
                        self.__active = True
                        self.fill("black")
                        self.text_surf = font_bold.render(self.text, 0, "white")
