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

    def set_pos(self, pos: Tuple[int, int]) -> None:
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
    def get_moves(self) -> List[int]:
        pass

    @abstractmethod
    def move_piece(self, pos: Tuple[int, int]) -> bool:
        pass


class Pawn(Piece):
    def __init__(self, colour: str, pos: Tuple[int, int]) -> None:
        Piece.__init__(self, colour, pos)
        self.has_moved = False

    def get_moves(self, current_player: int) -> List[int]:
        moves = []
        if current_player == 0 and self.get_colour() == 'white':
            moves = self.get_moves_white()
        elif current_player == 1 and self.get_colour() == 'black':
            moves = self.get_moves_black()
        return moves

    def get_moves_white(self) -> List[int]:
        moves = []
        moves.append((self.pos[0], self.pos[1] - 1))
        if not self.has_moved:
            moves.append((self.pos[0], self.pos[1] - 2))
        return moves

    def get_moves_black(self) -> List[int]:
        moves = []
        moves.append((self.pos[0], self.pos[1] + 1))
        if not self.has_moved:
            moves.append((self.pos[0], self.pos[1] + 2))
        return moves

    def move_piece(self, current_player: int, pos: Tuple[int, int]) -> bool:
        new_pos = next((position for position in self.get_moves(current_player) if pos == position), None)
        if new_pos is not None:
            self.set_pos(pos)
            self.has_moved = True
            return True
        return False


class Knight(Piece):
    def get_moves(self) -> List[int]:
        pass

    def move_piece(self, pos: Tuple[int, int]) -> bool:
        pass


class Bishop(Piece):
    def get_moves(self) -> List[int]:
        pass

    def move_piece(self, pos: Tuple[int, int]) -> bool:
        pass


class Rook(Piece):
    def get_moves(self) -> List[int]:
        pass

    def move_piece(self, pos: Tuple[int, int]) -> bool:
        pass


class King(Piece):
    def get_moves(self) -> List[int]:
        pass

    def move_piece(self, pos: Tuple[int, int]) -> bool:
        pass


class Queen(Piece):
    def get_moves(self) -> List[int]:
        pass

    def move_piece(self, pos: Tuple[int, int]) -> bool:
        pass
