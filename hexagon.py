# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 14:07:18 2022
@author: richa
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from tokenize import String
from typing import List
from typing import Tuple
from xmlrpc.client import Boolean
import datetime
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
                self.answer_seq.append('T')
                self.is_answered_true = True
                self.answer_colour = (0, 255, 0)     # green colour
            else: 
                self.answer_seq.append('F')
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

