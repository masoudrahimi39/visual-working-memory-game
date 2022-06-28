from __future__ import annotations
from sqlite3 import Timestamp
from typing import List
from typing import Tuple
from wsgiref.headers import Headers
from xmlrpc.client import Boolean
from hexagon import HexagonTile
import time
import pygame
import datetime
from pprint import pprint
import math
from buttons import Title

class Task:
    def __init__(self, indices_target, difficulty=10, user_id=10, num_x=6, num_y=4, show_time=2, position_init=(763, 300), R_hexagon=70):
        '''
            sequence_response_time: list[float, float, ...]: each float is in second. 
                first element : delta_time between start answering and ffirst click
                second element : delta_time between last click and current click 
        '''

        self.indices_target: list(int, ...) = indices_target
        self.n_target: int = len(indices_target)
        self.difficulty: float = difficulty
        self.num_x: int = num_x
        self.num_y: int = num_y
        self.show_time: int = show_time
        self.position_init: Tuple(int, int) = position_init
        self.hexagons:List(HexagonTile, HexagonTile, ...) = self.creat_task(R_hexagon)        # call instance method
        self.user_id = user_id                            # unique id 
        
        # based on user answer
        self.start_showing_task_ts: Timestamp = None                 # time of showing the task to user; used for ordering
        self.start_answering_ts: Timestamp = None                    # time of showing the white cells to user to get his answer
        self.indices_answer: List(int, ...) = []
        self.sequence_answer: List(int, ...) = []                         
        self.sequence_response_time: List(Timestamp, ...) = []                 
        self.num_true: int = None                              
        self.num_false: int = None
        self.is_wined: Boolean = None                              # boolean, True: all correct ans, Fasle: at least one incorrect
        self.score: float = None
        self.end_answering_ts: Timestamp = None

    def run_guiding_task(self, screen):
        title_bnt = Title(screen, clr_txt=(0,59,102), clr_brdr='white', show_up_txt='guiding trials')
        endTime = datetime.datetime.now() + datetime.timedelta(seconds=self.show_time)
        terminated = False
        while not terminated:
            title_bnt.draw()
            self.render_task(screen)
            for event in pygame.event.get():  
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            terminated = True
            if datetime.datetime.now() >= endTime:
                break

        # show the white screen to the user in order to get his/her answer
        terminated = False              # if answering is terminated or not
        clicked_hexagon_id = set()
        # cnt = 0
        while not terminated:
            for event in pygame.event.get():  
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        terminated = True              
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

    def run_task(self, screen):
        endTime = datetime.datetime.now() + datetime.timedelta(seconds=self.show_time)
        self.start_showing_task_ts = time.time()
        terminated = False
        while not terminated:
            self.render_task(screen)
            # TODO: delete below lines
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        terminated = True
            if datetime.datetime.now() >= endTime:
                break

        # show the white screen to the user in order to get his/her answer
        terminated = False              # if answering is terminated or not
        clicked_hexagon_id = set()
        cnt = 0
        while not terminated:
            # TODO: del 3 below lines 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        terminated = True
                
                # handle MOUSEBUTTONUP
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    # time the currect click
                    t_current_click = time.time()
                    pos = pygame.mouse.get_pos()           # position of the mouse clicke; (x, y)
                    # find the hexagon which the user clicked on
                    for hexagon in self.hexagons:
                        if hexagon.collide_with_point(pos) and id(hexagon) not in clicked_hexagon_id :

                            # append response time to sequence_response_time
                            if len(clicked_hexagon_id) == 0:           # if it is first click of user
                                self.sequence_response_time.append(t_current_click - self.start_answering_ts)
                                t_last_click = t_current_click
                            else:
                                self.sequence_response_time.append(t_current_click - t_last_click)
                                t_last_click = t_current_click

                            # append index of the clicked hexagon to indices_answer
                            self.indices_answer.append(hexagon.index)
                            clicked_hexagon_id.add(id(hexagon))

                            # append this click data into sequenc_answer (s.th. like this: 'TTTF')
                            if hexagon.is_answered_true == True:
                                self.sequence_answer.append(1)
                            elif hexagon.is_answered_true == False:
                                self.sequence_answer.append(0)
                            break
                
                    if len(clicked_hexagon_id) == len(self.indices_target):
                        terminated = True

            self.render_answer(screen)
            
            if cnt == 0:     # at the moment that answering screen is shown
                cnt += 1
                self.start_answering_ts = time.time()
        # end of answering to current task
        self.end_of_task()
        time.sleep(2)

        return self.score

    def creat_task(self, R_hexagon) -> List[HexagonTile]:
        """Creates a hexaogonal tile map of size num_x * num_y"""

        # determine if first cell is yellow or white
        temp = True if 0 in self.indices_target else False
        hex_counter = 0
        leftmost_hexagon = HexagonTile(is_target_cell=temp, position=self.position_init, index=hex_counter, radius=R_hexagon)  # TODO: change the position
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
        
    def end_of_task(self):
        self.end_answering_ts = time.time()
        self.num_true = self.sequence_answer.count(1)
        self.num_false = self.sequence_answer.count(0)
        self.is_wined = 1 if self.num_true == self.n_target else 0
        self.score = self.num_true / self.n_target


def task_param_based_on_screen(screen, num_x=6, num_y=4):
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
    for i in [(2, 7, 13, 20), (1, 2, 3, 4)]:
        task_obj = Task(indices_target=i, position_init=position_init, R_hexagon=R_hexagon)
        # task_obj.run_task(screen)
        task_obj.run_guiding_task(screen)
        # pprint(vars(task_obj))
        # break
    pygame.display.quit()