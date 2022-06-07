from __future__ import annotations
from typing import List
from typing import Tuple
from hexagon import HexagonTile
import datetime


class Task:
    def __init__(self, indices_to_1, num_x=6, num_y=4, show_time=2):

        self.indices_to_1 = indices_to_1
        self.num_x = num_x
        self.num_y = num_y
        self.show_time = show_time
        self.hexagons = self.creat_task()                 # call instance method
        self.user_id = None                               # unique id 
        
        # based on user answer
        self.task_showing_datetime = None                 # time of showing the task to user; used for ordering
        self.indices_answer = []
        self.sequence_answer = []                         # string like: TTTTFF
        self.num_task_played = None
        self.response_time_seq = None
        self.num_true = None
        self.num_false = None
        self.is_wined = None                              # boolean, True: all correct ans, Fasle: at least one incorrect


    
    def creat_task(self) -> List[HexagonTile]:
        """Creates a hexaogonal tile map of size num_x * num_y"""

        # determine if first cell is yellow or white
        temp = True if 0 in self.indices_to_1 else False
        hex_counter = 0
        leftmost_hexagon = HexagonTile(is_target_cell=temp, position=(200, 200), index=hex_counter)  # TODO: change the position
        hexagons = [leftmost_hexagon]
        gap = 0
        # iterate over rows
        for x in range(self.num_y):  # x is the row number
            if x:
                # alternate between bottom left and bottom right vertices of hexagon above
                index = 2 if x % 2 == 1 else 4
                position = leftmost_hexagon.vertices[index]
                position = (position[0], position[1]+gap)

                # determine if current cell is target or not (yellow or white)
                is_target_cell = True if hex_counter in self.indices_to_1 else False
                leftmost_hexagon = HexagonTile(is_target_cell=is_target_cell, position=position, index=hex_counter)
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
                position = (position[0]+2*gap, position[1])
                
                # determine if current cell is target or not (yellow or white)
                is_target_cell = True if hex_counter in self.indices_to_1 else False
                hexagon = HexagonTile(is_target_cell=is_target_cell, position=position, index=hex_counter)
                hexagons.append(hexagon)
                hex_counter +=1
      
        return hexagons

    # def set_task_showing_datetime(self):
    #     self.task_showing_datetime = datetime.datetime.now()

    def append_sequence_answer(self, T_or_F):
        # self.sequence_answer = self.sequence_answer + T_or_F
        self.sequence_answer.append(T_or_F)

    # def answer_task(self):