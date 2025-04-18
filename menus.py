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





#____ MENUS _____

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



        def click_event(self):
                """
                Handles the click event in the menus\n
                ::INPUT::
                        -Event: Clicking event

                ::OUTPUT::
                        -If click outside menus -> "False"
                        -If click inside menus -> "True"
                """
                #Click Event
                clicked_menu = ""
                click_position = pygame.mouse.get_pos()

                #Check if its inside a menu
                for menu in self.menus:
                        if  coord_inside_surf(click_position, menu.position, menu.dimmension):
                                clicked_menu = menu
                                break
                if clicked_menu == "": #If no menu was reached
                        return False

                #Check if its inside a button
                for button in clicked_menu.buttons:
                        # The coord of the button are relative to the menu so must be adjusted
                        relative_click_position = (click_position[0] -menu.position[0], click_position[1] -menu.position[1])
                        if coord_inside_surf(relative_click_position, button.position, button.size):
                                button.change_active()
                
                return True


        def render_menus(self):
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

        
        def reset_all_buttons(self):
                """
                Sets all buttons to the inactive state
                """
                for menu in self.menus:
                        for button in menu.buttons:
                                button.change_active(False)


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

                


        def create_button(self, position: tuple[int,int], size: tuple[int,int], text:str, active:bool=False)-> "Button":
                """
                Creates a button in the Menu.\n
                ::INPUT::
                        Position: Position of the button, relative to the surface
                        Size: Size of the button
                        Text: Text to be displayed in the button
                        Active: Sets the button starting value
                ::OUTPUT::
                        Returns the created instance
                """
                new_button = Button(position, size, text, active)
                self.buttons.append(new_button)
                return new_button








# _________ BUTTONS _________

class Button(pygame.Surface):
        def __init__(self, position: tuple[int,int], size: tuple[int,int], text:str, active:bool=False):
                """
                Generates a new button\n
                ::INPUT::
                        Position: Position of the button, relative to the surface
                        Size: Size of the button
                        Text: Text to be displayed in the button
                        Active: Sets the button starting value
                """
                self.position = position
                self.size = size
                self.text = text
                self.active = active

                #Text
                self.text_surf = font_normal.render(self.text, 0, "black")
                self.text_position = ( (self.size[0] - self.text_surf.get_width())/2 , (self.size[1] - self.text_surf.get_height())/2 )
                
                super().__init__(self.size)
                # Color changes 2 times so that it can be applied but not changed
                self.change_active()
                self.change_active()
        


        def change_active(self, to:bool=None):
                """
                Changes the button from active to inactive or inverse\n
                Also changes the button colour.
                ::INPUT::
                        To: indicates to which state to change, if nothing it will alternate
                """

                if self.active and to != True:       #Changes to inactive
                        self.active = False
                        self.fill("dark gray")
                        self.text_surf = font_normal.render(self.text, 0, "black")
                elif to != False:                   #Changes to active
                        self.active = True
                        self.fill("black")
                        self.text_surf = font_bold.render(self.text, 0, "white")
