from __future__ import annotations
import math
from dataclasses import dataclass, field
# from tokenize import String
from typing import List
from typing import Tuple
from xmlrpc.client import Boolean
import pygame


@dataclass
class HexagonTile:
    """source: https://github.com/rbaltrusch/pygame_examples/tree/master/code/hexagonal_tiles """
    is_target_cell : Boolean
    position: Tuple[float, float]
    index: int
    radius: float 
    is_clicked_as_answer: Boolean = False
    is_answered_true: Boolean = None
    clr_answer: Tuple[int, int, int] = (255, 255, 255)       # answer color of white
    
    def __post_init__(self):
        self.clr_hex = (255, 255, 255) if self.is_target_cell == False else (255,215,0)
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
                self.is_answered_true = True
                self.clr_answer = (0, 255, 0)     # green clr
            else: 
                self.is_answered_true = False
                self.clr_answer = (255, 0, 0)     # red clr
            return True
        else:
            return False


    def render(self, screen) -> None:
        """Renders the hexagon on the screen"""
        pygame.draw.polygon(screen, (self.highlight_clr), self.vertices)

    def render_answer(self, screen) -> None:
        """Renders the hexagon on the screen"""
        pygame.draw.polygon(screen, (self.clr_answer), self.vertices)

    def render_brdr(self, screen, border_clr=(0, 0, 0)) -> None:
        """Draws a border around the hexagon with the specified clr"""
        pygame.draw.aalines(screen, border_clr, closed=True, points=self.vertices)

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
    def highlight_clr(self) -> Tuple[int, ...]:
        return tuple(x for x in self.clr_hex)

