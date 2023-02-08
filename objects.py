import pygame
from abc import ABC
from typing import Tuple
from pathlib import Path


class Piece(ABC):
    def __init__(self, colour: str, pos: Tuple[int, int]):
        self.colour = colour
        self.pos = pos

    def get_colour(self) -> str:
        return self.colour

    def get_pos(self) -> Tuple[int, int]:
        return self.pos

    def set_pos(self, pos: Tuple[int, int]):
        self.pos = pos

    def get_class_name(self) -> str:
        return self.__class__.__name__

    def getImage(self) -> pygame.Surface:
        rel_path = '\\sprites\\{}\\{}.png'.format(self.colour, self.get_class_name())
        source_path = Path(__file__).resolve()
        source_dir = source_path.parent
        piece = pygame.image.load(source_dir.__str__() + rel_path)
        return pygame.transform.rotozoom(piece, 0, 0.45)


class Pawn(Piece):
    pass


class Knight(Piece):
    pass


class Bishop(Piece):
    pass


class Rook(Piece):
    pass


class King(Piece):
    pass


class Queen(Piece):
    pass
