import pygame


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

        
        def flip(self, click_event:pygame.event.Event):
                """
                Executes all needed functions for each frame
                        -Creating new lines
                        -Printing the lines to the screen
                ::INPUT::
                        -click_event: Click event
                """
                #Handle click Event
                if click_event != None:
                        self.__create_line(click_event)


                self.__render_drawings()
                
        
        def __render_drawings(self):
                """
                Prints the drawings in to the instance's screen (self.screen)
                """
                #Draws the completed lines
                for line in self.lines:
                        pygame.draw.line(self.screen, "blue", line[0], line[1])
                #Draws the incomplete lines
                if len(self.new_line) != 0:
                        pygame.draw.line(self.screen,"blue", self.new_line[0], pygame.mouse.get_pos())
                

        def __create_line(self, click_event:pygame.event.Event):
                """
                Creates new lines based on the clicks
                ::INPUT::
                        -Click_event: Event of "mousebuttondown"
                """
                click_position = pygame.mouse.get_pos()
                self.new_line.append(click_position)
                if len(self.new_line) == 2:
                        self.lines.append(self.new_line.copy())
                        self.new_line.pop(0)


