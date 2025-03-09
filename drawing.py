import pygame
from math import sqrt, asin, pi



class Drawing:
        def __init__(self, screen: pygame.Surface):
                """
                Used for drawing on the screen\n
                ::INPUT::
                        Screen: Surface to be written on
                """
                self.lines = []
                self.new_line = [] #Contains the points that dont form a line yet
                self.screen = screen
                self.button = False #State of the corresponding button (inital state doesnt affect)



        def flip(self, click_event:bool, button_active: bool):
                """
                Executes all needed functions for each frame
                        -Creating new lines
                        -Printing the lines to the screen
                ::INPUT::
                        -click_event: True if a click event occurred
                        -button: True if the corresponding button is active
                """
                self.button = button_active

                if button_active: # If drawing button is active
                        #Autoaim
                        autoaim_coords, point_autoaim = self.__autoaim()

                        #Create new lines
                        if click_event:
                                self.__create_line(autoaim_coords, point_autoaim)

                        #Render         
                        self.__render_drawings(autoaim_coords, point_autoaim)

                else:   #If the drawing button is inactive
                        self.new_line.clear()
                        self.__render_drawings((0,0), False)


        def __render_drawings(self, autoaim_coords:tuple[int,int], point_autoaim:bool):
                """
                Prints the drawings in to the instance's screen (self.screen)\n
                ::INPUT::
                        -Autoaim_coords: Mouse position modified by "__autoaim__"
                        -Point_autoaim: True if point auto aim was used, used for drawing autoaim circle
                """
                #Draws the completed lines
                for line in self.lines:
                        pygame.draw.line(self.screen, "blue", line[0], line[1])

                #Draws the incomplete lines
                if len(self.new_line) != 0:
                        pygame.draw.line(self.screen,"blue", self.new_line[0], autoaim_coords)

                #Draws the point of the autoaim
                if point_autoaim:
                        pygame.draw.circle(self.screen, "blue", autoaim_coords, 5)



        def __create_line(self, autoaim_coords:tuple[int,int], point_autoaim: bool):
                """
                Creates new lines based on the clicks\n
                ::INPUT::
                        -Autoaim_coords: Mouse position modified by "__autoaim__"
                        -Auto_aimed: True if autoaim
                """


                self.new_line.append(autoaim_coords)
                #If the line is complete
                if len(self.new_line) == 2:
                        self.lines.append(self.new_line.copy())
                        self.new_line.pop(0) #The next line beggins from the last one

                        # If point_autoaim was used, end the drawing
                        if point_autoaim:
                                self.new_line.clear()



        def __autoaim(self)-> tuple[int,int]:
                """
                Auto-aims when close to points or to 90º angles
                        -Also renders a point when autoaim to a point is active
                ::RETURN::
                        -If autoaim is active
                                -By a point: returns point and "TRUE"
                                -By angle: Returns point and "NONE"
                        -If autoaim is inactive returs unmodified location and "FALSE"
                        
                """
                mouse_position = pygame.mouse.get_pos()

                point_autoaim_radius = 20 # Distance from a point so that autoaim works
                angle_autoaim = 5 # Degrees form 90º angle so that autoaim works
                angle_autoaim_radius = 20 #Distance min for angle autoaim to work

                # __Point autoaim__

                # Length for the range; if a new line is beein drawn avoids auto aiming at itself
                if len(self.new_line) !=0: #New line beeing drawn
                        lines_len = len(self.lines)-1
                else:
                        lines_len = len(self.lines)

                for i in range(lines_len): 
                        line = self.lines[i]
                        for point in line:
                                #Poitn is (x,y) coordenates
                                distance = sqrt((mouse_position[0] - point[0])**2 + (mouse_position[1] - point[1])**2)
                                
                                if distance < point_autoaim_radius:
                                        return point, True



                # __Angle autoaim__

                if len(self.new_line) != 0:
                        prev_point = self.new_line[-1]

                        dist_vect = (mouse_position[0]- prev_point[0], mouse_position[1]- prev_point[1])
                        dist = sqrt( dist_vect[0]**2 + dist_vect[1]**2)
                        if dist > angle_autoaim_radius:
                                angle = abs(asin( -dist_vect[1] / dist ) * 360 / (2 * pi))

                                if 0 < angle < angle_autoaim:
                                        autoaim_point = (mouse_position[0], prev_point[1])
                                        return autoaim_point, None

                                if angle > 90 - angle_autoaim:
                                        autoaim_point = (prev_point[0], mouse_position[1])
                                        return autoaim_point, None

                return mouse_position, False