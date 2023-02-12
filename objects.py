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

    def move_piece(self, pos: Tuple[int, int]) -> bool:
        new_pos = next((position for position in self.get_moves() if pos == position), None)
        if new_pos is not None:
            piece_on_new_pos = Piece_Handler.get_piece_on_board(pos)
            if piece_on_new_pos is not None:
                Piece_Handler.remove_piece(piece_on_new_pos)
            self.set_pos(pos)
            Piece_Handler.set_ghost_piece((-1, -1))
            return True
        return False

    def valid_take(self, pos) -> bool:
        piece_taken = Piece_Handler.get_piece_on_board(pos)
        return piece_taken is not None and self.colour != piece_taken.colour

    @abstractmethod
    def get_moves(self) -> List[int]:
        pass


class Pawn(Piece):
    def __init__(self, colour: str, pos: Tuple[int, int]) -> None:
        Piece.__init__(self, colour, pos)
        self.has_moved = False

    def get_moves(self) -> List[int]:
        moves = []
        black_white = -1 if self.get_colour() == 'white' else 1
        if Piece_Handler.get_piece_on_board((self.pos[0], self.pos[1] + black_white)) is None:
            moves.append((self.pos[0], self.pos[1] + black_white))
        if not self.has_moved and Piece_Handler.get_piece_on_board((self.pos[0], self.pos[1] + 2 * black_white)) is None:
            moves.append((self.pos[0], self.pos[1] + 2 * black_white))
        if self.valid_take((self.pos[0] + 1, self.pos[1] + black_white)) or Piece_Handler.get_ghost_piece() == (self.pos[0] + 1, self.pos[1] + black_white):
            moves.append((self.pos[0] + 1, self.pos[1] + black_white))
        if self.valid_take((self.pos[0] - 1, self.pos[1] + black_white)) or Piece_Handler.get_ghost_piece() == (self.pos[0] - 1, self.pos[1] + black_white):
            moves.append((self.pos[0] - 1, self.pos[1] + black_white))
        return moves

    def move_piece(self, pos: Tuple[int, int]) -> bool:
        old_pos = self.pos
        ghost_piece = Piece_Handler.get_ghost_piece()
        valid_move = super().move_piece(pos)
        black_white = 1 if self.get_colour() == 'white' else -1
        if not self.has_moved and valid_move and abs(old_pos[1] - self.pos[1]) == 2:
            Piece_Handler.set_ghost_piece((self.pos[0], self.pos[1] + black_white))
        self.has_moved = True
        if self.pos == ghost_piece:
            Piece_Handler.remove_piece(Piece_Handler.get_piece_on_board((self.pos[0], self.pos[1] + black_white)))
        return valid_move


class Knight(Piece):
    def get_moves(self) -> List[int]:
        pass


class Bishop(Piece):
    def get_moves(self) -> List[int]:
        pass


class Rook(Piece):
    def get_moves(self) -> List[int]:
        pass


class King(Piece):
    def get_moves(self) -> List[int]:
        pass


class Queen(Piece):
    def get_moves(self) -> List[int]:
        pass


class Piece_Handler():
    pieces = []
    ghost = (-1, -1)

    @staticmethod
    def init_pieces() -> None:
        for i in range(8):
            Piece_Handler.pieces.append(Pawn("white", (i, 6)))
            Piece_Handler.pieces.append(Pawn("black", (i, 1)))
        Piece_Handler.pieces.append(Rook("black", (0, 0)))
        Piece_Handler.pieces.append(Rook("black", (7, 0)))
        Piece_Handler.pieces.append(Rook("white", (0, 7)))
        Piece_Handler.pieces.append(Rook("white", (7, 7)))
        Piece_Handler.pieces.append(Knight("black", (1, 0)))
        Piece_Handler.pieces.append(Knight("black", (6, 0)))
        Piece_Handler.pieces.append(Knight("white", (1, 7)))
        Piece_Handler.pieces.append(Knight("white", (6, 7)))
        Piece_Handler.pieces.append(Bishop("black", (2, 0)))
        Piece_Handler.pieces.append(Bishop("black", (5, 0)))
        Piece_Handler.pieces.append(Bishop("white", (2, 7)))
        Piece_Handler.pieces.append(Bishop("white", (5, 7)))
        Piece_Handler.pieces.append(King("black", (4, 0)))
        Piece_Handler.pieces.append(King("white", (4, 7)))
        Piece_Handler.pieces.append(Queen("black", (3, 0)))
        Piece_Handler.pieces.append(Queen("white", (3, 7)))

    @staticmethod
    def get_pieces() -> List[Piece]:
        return Piece_Handler.pieces

    def get_piece_on_board(pos: Tuple[int]) -> Piece:
        return next((piece for piece in Piece_Handler.get_pieces() if piece.get_pos() == pos), None)

    def remove_piece(piece: Piece) -> None:
        Piece_Handler.pieces.remove(piece)

    def set_ghost_piece(pos) -> None:
        Piece_Handler.ghost = pos

    def get_ghost_piece() -> Tuple[int]:
        return Piece_Handler.ghost
