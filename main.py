# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 13:50:07 2022
@author: richa
"""
import random
from typing import List
from typing import Tuple
import time

import pygame
from hexagon import FlatTopHexagonTile
from hexagon import HexagonTile
import os


# pylint: disable=no-member


def create_hexagon(target_cell, position, radius=50, flat_top=False) -> HexagonTile:
    """Creates a hexagon tile at the specified position"""
    class_ = FlatTopHexagonTile if flat_top else HexagonTile
        # TODO: change colour in the below line in order to change the cell's color    # gold color rgb : (255,215,0)
    return class_(target_cell, position, radius) 



# def get_random_colour(min_=150, max_=255) -> Tuple[int, ...]:
#     """Returns a random RGB colour with each component between min_ and max_"""
#     return tuple(random.choices(list(range(min_, max_)), k=3))

def init_hexagons(indices_to_1, num_x=6, num_y=4, flat_top=False) -> List[HexagonTile]:
    """Creates a hexaogonal tile map of size num_x * num_y"""
    # pylint: disable=invalid-name

    # determine if first cell is yellow or white
    temp = True if 0 in indices_to_1 else False
    leftmost_hexagon = create_hexagon(target_cell=temp, position=(200, 200), flat_top=flat_top)
    hexagons = [leftmost_hexagon]
    hex_counter = 0
    gap = 0
    for x in range(num_y):  # x is the row number
        if x:
            # alternate between bottom left and bottom right vertices of hexagon above
            index = 2 if x % 2 == 1 or flat_top else 4
            position = leftmost_hexagon.vertices[index]
            position = (position[0], position[1]+gap)

            if hex_counter in indices_to_1:
                leftmost_hexagon = create_hexagon(True, position, flat_top=flat_top)
            else:
                leftmost_hexagon = create_hexagon(False, position, flat_top=flat_top)
            hexagons.append(leftmost_hexagon)
            hex_counter +=1
        else:
            hex_counter +=1

        # place hexagons to the left of leftmost hexagon, with equal y-values.
        hexagon = leftmost_hexagon
        
        for i in range(1, num_x):   # i is the column number
            x, y = hexagon.position  # type: ignore    
            position = (x + hexagon.minimal_radius * 2, y)
            position = (position[0]+2*gap, position[1])
            
            if hex_counter in indices_to_1:
                hexagon = create_hexagon(True, position, flat_top=flat_top)
            else:
                hexagon = create_hexagon(False, position, flat_top=flat_top)
            hexagons.append(hexagon)
            hex_counter +=1
            
    return hexagons


def render(screen, hexagons):
    """Renders hexagons on the screen"""
    screen.fill((255, 255, 255))
    for hexagon in hexagons:
        hexagon.render(screen)
        hexagon.render_highlight(screen, border_colour=(150, 0, 0))


    # draw borders around colliding hexagons and neighbours
    # if pygame.mouse.get_pressed():

    #     mouse_pos = pygame.mouse.get_pos()
        # print(mouse_pos)
    # colliding_hexagons = [
    #     hexagon for hexagon in hexagons if hexagon.collide_with_point(mouse_pos)
    # ]
    # for hexagon in colliding_hexagons:
    #     for neighbour in hexagon.compute_neighbours(hexagons):
    #         neighbour.render_highlight(screen, border_colour=(100, 100, 100))
        # hexagon.render_highlight(screen, border_colour=(100, 100, 100))
    pygame.display.flip()


def main():
    """Main function"""
    pygame.init()
    screen = pygame.display.set_mode((750, 750))
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    indices_to_1 = [1, 5, 6, 7, 8, 11, 23]
    hexagons = init_hexagons(indices_to_1, flat_top=False)
    # print(hexagons)
    terminated = False

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
            if event.type == pygame.MOUSEBUTTONUP:
                # get position of the mouse clicke (x, y)
                pos = pygame.mouse.get_pos()
                # find the hexagn which the user clicked on
                clicked_sprites = [hexagon for hexagon in hexagons if hexagon.collide_with_point(pos)]
                if clicked_sprites:
                    clicked_hexagon_id.add(id(clicked_sprites[0]))
                    # print(clicked_hexagon_id)
                    print(id(clicked_sprites[0]))
                    if len(clicked_hexagon_id) == len(indices_to_1):
                        time.sleep(1)
                        terminated = True
                        
                
                # do something with the clicked sprites...


        render(screen, hexagons)
        clock.tick(50)
    pygame.display.quit()


if __name__ == "__main__":
    main()