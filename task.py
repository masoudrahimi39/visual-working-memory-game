from __future__ import annotations
from sqlite3 import Timestamp
from typing import List
from typing import Tuple
from xmlrpc.client import Boolean
from hexagon import HexagonTile
import time
import pygame
import datetime
from pprint import pprint
import math
from buttons import Title


class Task:
    def __init__(self, *, indices_target, dda_mthd, user_info, difficulty, num_x, 
                num_y, show_time, position_init, R_hexagon, tracker, is_eye_tracker):
        '''
            is_eye_tracker: Boolean: If True, there is a eye tracker device else there isn't.
            tracker: Eye tracker object; it is used if is_eye_tracker == True, else it is ignored.
            indices_target: tuple: used to create the task. It contains indices of the cells which should be target cells. 
                    indexing start from up left to right and then down
            dda_mthd: str: it determines which method used for DDA
            user_info: dict: it is the user data. all elements of user_info are added to the __dict__ attribute of the obj
            difficutly: the correspondance difficutly of the task.
            num_x: number of columns in the task table
            num_y: number of the rows in the task table
            show_time: int: the task is shown to the user to memorize it for show_time seconds.
            position_inti: the position of the most-upper-left hexagon in the task; it is passed to the HexagonTile
            R_hexagon: float: the Radiu of the hexagon; it is passed to the HexagonTile
            sequence_response_time: list[float, float, ...]: each float is in second. 
                first element : delta_time between start answering and first click
                second element : delta_time between last click and current click 
        '''
        # update the __dict__ of the this object with the user_info
        self.__dict__.update(user_info)
        self.is_eye_tracker = is_eye_tracker
        self.tracker = tracker 
        self.indices_target: list(int, ...) = indices_target
        self.dda_mthd = dda_mthd
        self.difficulty: float = difficulty
        self.num_x: int = num_x
        self.num_y: int = num_y
        self.show_time: int = show_time
        self.position_init: Tuple(int, int) = position_init
        self.R_hexagon = R_hexagon
        self.n_target: int = len(indices_target)
        self.hexagons:List(HexagonTile, HexagonTile, ...) = self.creat_task(R_hexagon)        # call instance method
        
        # based on user answer
        self.start_showing_task_ts: Timestamp = None                 # time of showing the task to user; used for ordering
        self.end_showing_task_ts: Timestamp = None
        self.start_answering_ts: Timestamp = None                    # time of showing the white cells to user to get his answer
        self.indices_answer: List(int, ...) = []
        self.sequence_answer: List(int, ...) = []                         
        self.sequence_response_time: List(Timestamp, ...) = []                 
        self.num_true: int = None                              
        self.num_false: int = None
        self.is_wined: Boolean = None                                # boolean, True: all correct ans, Fasle: at least one incorrect
        self.score: float = None
        self.end_answering_ts: Timestamp = None


    def run_task(self, screen):
        ''' '''
        endTime = datetime.datetime.now() + datetime.timedelta(seconds=self.show_time)
        self.start_showing_task_ts = time.time()
        terminated = False
        while not terminated:    # memorization mode 
            # TODO: is usage of tracker true here
            if self.is_eye_tracker == True:
                event_tag_ET = str(self.task_nmbr) + '_MEMO'
                self.tracker.user_data(event_tag_ET)        # send event to eye tracker
            self.render_task(screen)
            if datetime.datetime.now() >= endTime:
                self.end_showing_task_ts = time.time()
                break

        # show the white screen to the user in order to get his/her answer
        terminated = False              # if answering is terminated or not
        clicked_hexagon_id = set()
        cnt = 0
        pygame.event.clear()
        while not terminated:    # recal mode
            # TODO: is usage of tracker true here
            if self.is_eye_tracker == True:
                # send event to eye tracker
                event_tag_ET = str(self.task_nmbr) + '_RECALL'
                self.tracker.user_data(event_tag_ET) 

            for event in pygame.event.get():
                if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                    t_current_click = time.time()          # the currect click time 
                    pos = pygame.mouse.get_pos()           # position of the mouse clicke; (x, y)
                    
                    # find the hexagon which the user clicked on
                    for hexagon in self.hexagons:
                        if hexagon.collide_with_point(pos) and id(hexagon) not in clicked_hexagon_id :

                            # append response time to sequence_response_time
                            if len(clicked_hexagon_id) == 0:           # if it is the first click of the user
                                self.sequence_response_time.append(t_current_click - self.start_answering_ts)
                                t_last_click = t_current_click
                            else:                                     # if it is not the first click of the user
                                self.sequence_response_time.append(t_current_click - t_last_click)
                                t_last_click = t_current_click

                            # append index of the clicked hexagon to indices_answer
                            self.indices_answer.append(hexagon.index)
                            clicked_hexagon_id.add(id(hexagon))

                            # append this click data into sequenc_answer
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
                start_warning_time = self.start_answering_ts + 5
                end_warning_time = start_warning_time + 2
            if time.time() > end_warning_time:
                try:
                    del warning_obj
                    screen.fill('white')
                except:
                    pass
    
            elif time.time() > start_warning_time:
                warning_obj = Title(screen, font_ratio_to_screen=25, clr_brdr='white', show_up_txt=f'{self.n_target-len(self.indices_answer)} more click')
                warning_obj.draw()
                
        # end of answering to current task
        self.end_of_task()
        time.sleep(2)

        return self.score

    def creat_task(self, R_hexagon) -> List[HexagonTile]:
        """Creates a hexaogonal tile map of size num_x * num_y correspondance to the indices_target and return a list of hexagons"""

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
        
    def end_of_task(self):
        ''' set some attributes value. delete some useless attributes'''
        self.end_answering_ts = time.time()
        self.num_true = self.sequence_answer.count(1)
        self.num_false = self.sequence_answer.count(0)
        self.is_wined = 1 if self.num_true == self.n_target else 0
        self.score = self.num_true / self.n_target
        delattr(self, 'hexagons')
        # TODO: maybe i should delete the tracker attribute
        # delattr(self, 'tracker')


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
    for i in [(1, 2, 3, 4, 33), (1, 3, 5, 9), (18, 17, 31), (0, 5, 8, 9, 11, 17, 20, 22, 30, 33, 35)]:
        task_obj = Task(indices_target=i, dda_mthd='nothing', user_info={}, difficulty=None, num_x=6, 
                        num_y=6, show_time=2, position_init=position_init, R_hexagon=R_hexagon,
                         tracker=None, is_eye_tracker=False)
        task_obj.run_task(screen)
        # pprint(vars(task_obj))
        # break
    pygame.display.quit()
