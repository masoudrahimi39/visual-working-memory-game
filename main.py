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



def main(indices_to_1):
    # creat an instance of task
    task_obj = Task(indices_to_1=indices_to_1)
    task_obj.creat_task()
    # task_obj.user_id =                       # UUID of the user

    # show the task to the player for task_obj.show_time seconds
    pygame.init()
    screen = pygame.display.set_mode((750, 750))
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    endTime = datetime.datetime.now() + datetime.timedelta(seconds=task_obj.show_time)
    task_obj.task_showing_datetime = datetime.datetime.now()
    while True:
        render_task(screen, task_obj.hexagons)
        if datetime.datetime.now() >= endTime:
            break
    pygame.display.quit()


    # show the white screen to the user in order to get his/her answer
    pygame.init()
    screen = pygame.display.set_mode((750, 750))
    clock = pygame.time.Clock()     # clock is starting at the time of showing white screen in order to get the user's answer

    terminated = False              # if answering is terminated or not
    clicked_hexagon_id = set()
    while not terminated:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    terminated = True
            
            # handle MOUSEBUTTONUP
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:



                pos = pygame.mouse.get_pos()           # position of the mouse clicke; (x, y)
                # find the hexagon which the user clicked on
                for hexagon in task_obj.hexagons:
                    if hexagon.collide_with_point(pos) and id(hexagon) not in clicked_hexagon_id :
                        task_obj.indices_answer.append(hexagon.index)
                        clicked_hexagon_id.add(id(hexagon))
                        # add this click data into sequenc_answer (s.th. like this: 'TTTF')
                        if hexagon.is_answered_true == True:
                            task_obj.append_sequence_answer('T')
                        elif hexagon.is_answered_true == False:
                            task_obj.append_sequence_answer('F')
                        break

                if len(clicked_hexagon_id) == len(indices_to_1):
                    terminated = True


        render_answer(screen, task_obj.hexagons)
        clock.tick(50)


    time.sleep(1)
    pygame.display.quit()
    # print(task_obj.sequence_answer)



if __name__ == "__main__":
    main([0, 1, 2, 3])
    