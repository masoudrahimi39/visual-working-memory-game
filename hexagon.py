# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 14:07:18 2022
@author: richa
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List
from typing import Tuple
from xmlrpc.client import Boolean

import pygame


@dataclass
class HexagonTile:
    """Each Hexagon is one object from HexagonTile"""

    is_target_cell : Boolean
    position: Tuple[float, float]
    radius: float = 50
    is_clicked_as_answer: Boolean = False
    is_answered_true: Boolean = None
    answer_colour: Tuple[int, int, int] = (255, 255, 255)       # answer color of white


    def __post_init__(self):
        self.colour = (255, 255, 255) if self.is_target_cell == False else (255,215,0)
        self.vertices = self.compute_vertices()
        # self.is_clicked_as_answer = self.click_answer()[0]
        # self.is_answered_true = self.click_answer()[1]
        # self.asnwer_colour = self.click_answer()[2]


    def compute_vertices(self) -> List[Tuple[float, float]]:
        """Returns a list of the hexagon's vertices as x, y tuples"""
        # pylint: disable=invalid-name
        x, y = self.position
        half_radius = self.radius / 2
        minimal_radius = self.minimal_radius
        return [
            (x, y),
            (x - minimal_radius, y + half_radius),
            (x - minimal_radius, y + 3 * half_radius),
            (x, y + 2 * self.radius),
            (x + minimal_radius, y + 3 * half_radius),
            (x + minimal_radius, y + half_radius),
        ]


    def collide_with_point(self, point: Tuple[float, float]) -> bool:
        """Returns True if distance from centre to point is less than horizontal_length"""
        if math.dist(point, self.centre) < self.minimal_radius :
            self.is_clicked_as_answer = True
            if self.is_target_cell == True:       # if this cell is s target cell
                self.is_answered_true = True
                self.answer_colour = (0, 255, 0)     # green colour
            else: 
                self.is_answered_true = False
                self.answer_colour = (255, 0, 0)     # red colour
            return True
        else:
            return False


    def render(self, screen) -> None:
        """Renders the hexagon on the screen"""
        pygame.draw.polygon(screen, (self.highlight_colour), self.vertices)

    def render_answer(self, screen) -> None:
        """Renders the hexagon on the screen"""
        pygame.draw.polygon(screen, (self.answer_colour), self.vertices)

    def render_highlight(self, screen, border_colour) -> None:
        """Draws a border around the hexagon with the specified colour"""
        pygame.draw.aalines(screen, border_colour, closed=True, points=self.vertices)

    @property
    def centre(self) -> Tuple[float, float]:
        """Centre of the hexagon"""
        x, y = self.position  # pylint: disable=invalid-name
        return (x, y + self.radius)

    @property
    def minimal_radius(self) -> float:
        """Horizontal length of the hexagon"""
        # https://en.wikipedia.org/wiki/Hexagon#Parameters
        return self.radius * math.cos(math.radians(30))

    @property
    def highlight_colour(self) -> Tuple[int, ...]:
        return tuple(x for x in self.colour)



@dataclass
class Task:
    """Task class"""
    indices_to_1: Tuple[int, ...]
    num_x: int = 6
    num_y: int = 4
    answer_indices: Tuple[int, ...] = None
    

    def __post_init__(self):
        self.task_hexagons = self.init_hexagons()
        # self.answer_hexagons = 
        # self.colour = (255, 255, 255) if self.is_target_cell == False else (255,215,0)
        # self.vertices = self.compute_vertices()


    def init_hexagons(self) -> List[HexagonTile]:
        """Creates a hexaogonal tile map of size num_x * num_y"""

        # determine if first cell is yellow or white
        temp = True if 0 in self.indices_to_1 else False
        leftmost_hexagon = HexagonTile(is_target_cell=temp, position=(200, 200))  # TODO: change the position
        hexagons = [leftmost_hexagon]
        hex_counter = 0
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
                leftmost_hexagon = HexagonTile(is_target_cell=is_target_cell, position=position)
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
                hexagon = HexagonTile(is_target_cell=False, position=position)
                hexagons.append(hexagon)
                hex_counter +=1
                
        return hexagons
