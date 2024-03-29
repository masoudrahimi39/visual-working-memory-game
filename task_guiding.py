from __future__ import annotations
from typing import List
from typing import Tuple
from hexagon import HexagonTile
import time
import pygame
import datetime
from pprint import pprint
import math
from buttons import Title


class TaskGuiding:
    def __init__(self, *, indices_target, num_x=6, num_y=6, show_time=2, position_init=(763, 300), R_hexagon=70):
        '''
            sequence_response_time: list[float, float, ...]: each float is in second. 
                first element : delta_time between start answering and ffirst click
                second element : delta_time between last click and current click 
        '''


        self.indices_target: list(int, ...) = indices_target
        self.n_target: int = len(indices_target)
        self.num_x: int = num_x
        self.num_y: int = num_y
        self.show_time: int = show_time
        self.position_init: Tuple(int, int) = position_init
        self.hexagons:List(HexagonTile, HexagonTile, ...) = self.creat_task(R_hexagon)        # call instance method                          # unique id 
        
        # based on user answer
        self.indices_answer: List(int, ...) = []


    def run_guiding_task(self, screen):
        title_bnt = Title(screen, clr_txt=(0,59,102), clr_brdr='white', show_up_txt='guiding trials')
        endTime = datetime.datetime.now() + datetime.timedelta(seconds=self.show_time)
        terminated = False
        while not terminated: 
            title_bnt.draw()
            self.render_task(screen)
            if datetime.datetime.now() >= endTime:
                break
        
        # show the white screen to the user in order to get his/her answer
        terminated = False              # if answering is terminated or not
        clicked_hexagon_id = set()
        
        pygame.event.clear()
        while not terminated:       
            for event in pygame.event.get():               
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = pygame.mouse.get_pos()           # position of the mouse clicke; (x, y)
                    # find the hexagon which the user clicked on
                    for hexagon in self.hexagons:
                        if hexagon.collide_with_point(pos) and id(hexagon) not in clicked_hexagon_id :
                            clicked_hexagon_id.add(id(hexagon))
                            break
                
                    if len(clicked_hexagon_id) == len(self.indices_target):
                        terminated = True
            title_bnt.draw()
            self.render_answer(screen)
        time.sleep(2)


    def creat_task(self, R_hexagon) -> List[HexagonTile]:
        """Creates a hexaogonal tile map of size num_x * num_y"""

        # determine if first cell is yellow or white
        temp = True if 0 in self.indices_target else False
        hex_counter = 0
        leftmost_hexagon = HexagonTile(is_target_cell=temp, position=self.position_init, index=hex_counter, radius=R_hexagon) 
        hexagons = [leftmost_hexagon]
        # iterate over rows
        for x in range(self.num_y):  # x is the row number
            if x:
                # alternate between bottom left and bottom right vertices of hexagon above
                index = 2 if x % 2 == 1 else 4
                position = leftmost_hexagon.vertices[index]
                position = (position[0], position[1])

                # determine if current cell is target or not (yellow or white)
                is_target_cell = True if hex_counter in self.indices_target else False
                leftmost_hexagon = HexagonTile(is_target_cell=is_target_cell, position=position, index=hex_counter, radius=R_hexagon)
                hexagons.append(leftmost_hexagon)
                hex_counter +=1
            else:
                hex_counter +=1

            # place hexagons to the left of leftmost hexagon, with equal y-values.
            hexagon = leftmost_hexagon
            
            # iterate over columns
            for i in range(1, self.num_x):   # i is the column number
                x, y = hexagon.position  # type: ignore    
                position = (x + hexagon.minimal_radius * 2, y)
                position = (position[0], position[1])
                
                # determine if current cell is target or not (yellow or white)
                is_target_cell = True if hex_counter in self.indices_target else False
                hexagon = HexagonTile(is_target_cell=is_target_cell, position=position, index=hex_counter, radius=R_hexagon)
                hexagons.append(hexagon)
                hex_counter +=1
      
        return hexagons

    def render_task(self, screen):
        for hexagon in self.hexagons:
            hexagon.render(screen)
            hexagon.render_brdr(screen)
        pygame.display.flip()

    def render_answer(self, screen):
        for hexagon in self.hexagons:
            hexagon.render_answer(screen)
            hexagon.render_brdr(screen)   
        pygame.display.flip()
        

def task_param_based_on_screen(screen, num_x=6, num_y=6):
    ''' input
        -------
            screen: pygame screen object
        output
        -------
            R_hexagon: radius of each hexagon based on screen size
            position_int: the postion of the most lef hexagon based on scren size'''
    screen_width, screen_height = screen.get_size()
    R_hexagon =  screen_width/25
    d_hexagon = 2 * R_hexagon * math.cos(math.radians(30))
    position_init = (screen_width/2 - (num_x-1.5)/2*d_hexagon, screen_height/2 - (num_y-0.5) * R_hexagon)
    return position_init, R_hexagon


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1919, 1079))  
    # get parameters to pass into the Task based on screen size
    position_init, R_hexagon = task_param_based_on_screen(screen)
    screen.fill('white') 
    for i in [(1, 2, 3, 4), (10, 12, 14, 30, 35), (0, 5, 8, 9, 11, 17, 20, 30, 31, 35)]:
        task_gd_obj = TaskGuiding(indices_target=i, num_x=6, num_y=6, position_init=position_init, R_hexagon=R_hexagon)
        task_gd_obj.run_guiding_task(screen)
        # pprint(vars(task_gd_obj))

    pygame.display.quit()