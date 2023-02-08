import pygame
from abc import ABC, abstractmethod
from typing import Tuple, List
from pathlib import Path


class Piece(ABC):
    def __init__(self, colour: str, pos: Tuple[int, int]) -> None:
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
        image = pygame.image.load(source_dir.__str__() + rel_path)
        return pygame.transform.rotozoom(image, 0, 0.45)

    @abstractmethod
    def get_moves() -> List[int]:
        pass


class Pawn(Piece):
    def __init__(self, colour: str, pos: Tuple[int, int]) -> None:
        Piece.__init__(self, colour, pos)
        self.has_moved = False

    def get_moves(self) -> List[int]:
        moves = []
        black_white = 1 if self.colour == "white" else -1
        moves.append((self.pos[0], self.pos[1] - (1 * black_white)))
        if not self.has_moved:
            moves.append((self.pos[0], self.pos[1] - (2 * black_white)))
        return moves


class Knight(Piece):
    def get_moves():
        pass


class Bishop(Piece):
    def get_moves():
        pass


class Rook(Piece):
    def get_moves():
        pass


class King(Piece):
    def get_moves():
        pass


class Queen(Piece):
    def get_moves():
        pass


class Circle:
    def __init__(self, pos) -> None:
        self.pos = pos

    def get_pos(self) -> Tuple[int, int]:
        return self.pos
