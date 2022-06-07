# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 13:50:07 2022
@author: richa
"""
import random
from typing import List
from typing import Tuple
import time
import datetime
import pygame
from task import Task
from hexagon import HexagonTile

from dataclasses import dataclass


# pylint: disable=no-member



def render_task(screen, hexagons):
    """Renders hexagons on the screen"""
    screen.fill((255, 255, 255))           # screen color of white
    for hexagon in hexagons:
        hexagon.render(screen)
        hexagon.render_highlight(screen, border_colour=(0, 0, 0))
    pygame.display.flip()
    
def render_answer(screen, hexagons):
    """Renders asnwer on the screen"""
    screen.fill((255, 255, 255))           # screen color of white
    for hexagon in hexagons:
        hexagon.render_answer(screen)
        hexagon.render_highlight(screen, border_colour=(0, 0, 0))   
    pygame.display.flip()


def init_hexagons(indices_to_1, num_x=6, num_y=4) -> List[HexagonTile]:
    """Creates a hexaogonal tile map of size num_x * num_y"""

    # determine if first cell is yellow or white
    temp = True if 0 in indices_to_1 else False
    leftmost_hexagon = HexagonTile(is_target_cell=temp, position=(200, 200))  # TODO: change the position
    hexagons = [leftmost_hexagon]
    hex_counter = 0
    gap = 0    
    
    # iterate over rows
    for x in range(num_y):  # x is the row number
        if x:
            # alternate between bottom left and bottom right vertices of hexagon above
            index = 2 if x % 2 == 1 else 4
            position = leftmost_hexagon.vertices[index]
            position = (position[0], position[1]+gap)

            # determine if current cell is target or not (yellow or white)
            is_target_cell = True if hex_counter in indices_to_1 else False
            leftmost_hexagon = HexagonTile(is_target_cell=is_target_cell, position=position)
            hexagons.append(leftmost_hexagon)
            hex_counter +=1
        else:
            hex_counter +=1

        # place hexagons to the left of leftmost hexagon, with equal y-values.
        hexagon = leftmost_hexagon
        
        # iterate over columns
        for i in range(1, num_x):   # i is the column number
            x, y = hexagon.position  # type: ignore    
            position = (x + hexagon.minimal_radius * 2, y)
            position = (position[0]+2*gap, position[1])
            
            # determine if current cell is target or not (yellow or white)
            is_target_cell = True if hex_counter in indices_to_1 else False
            hexagon = HexagonTile(is_target_cell=is_target_cell, position=position)
            hexagons.append(hexagon)
            hex_counter +=1
            
    return hexagons



def main():
    # creat an instance of task
    task_obj = Task(indices_to_1=[1, 2, 3, 23], num_x=6, num_y=4)

    # show the task to the player for show_time seconds
    pygame.init()
    screen = pygame.display.set_mode((750, 750))
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    show_time = 2
    endTime = datetime.datetime.now() + datetime.timedelta(seconds=show_time)
    while True:
        render_task(screen, task_obj.hexagons)
        if datetime.datetime.now() >= endTime:
            break
    pygame.display.quit()


    # show the white screen to the user in order to get his/her answer
    pygame.init()
    screen = pygame.display.set_mode((750, 750))
    clock = pygame.time.Clock()
    terminated = False              # if answer is terminated or not
    clicked_hexagon_id = set()
    # click_counter
    while not terminated:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    terminated = True
            
            # handle MOUSEBUTTONUP
            if event.type == pygame.MOUSEBUTTONUP:
                # get position of the mouse clicke (x, y)
                pos = pygame.mouse.get_pos()
                # find the hexagon which the user clicked on
                for hexagon in task_obj.hexagons:
                    
                    if hexagon.collide_with_point(pos):
                        
                        clicked_sprites = [hexagon]
                        print(clicked_sprites)
                        break
                if clicked_sprites:
                    clicked_hexagon_id.add(id(clicked_sprites[0]))
                    if len(clicked_hexagon_id) == len(indices_to_1):
                        # add answer sequence to the clicked_sprites
                        for hexagon in clicked_sprites:
                            hexagon.asn
                        terminated = True
                        
                
                # do something with the clicked sprites...


        render_answer(screen, hexagons)
        clock.tick(50)


    time.sleep(1)
    pygame.display.quit()
    

if __name__ == "__main__":
    main()