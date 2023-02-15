import pygame
from abc import ABC, abstractmethod
from typing import Tuple, List
from pathlib import Path
import itertools


class Piece(ABC):
    '''
        A class used to draw and move pieces

        ...

        Attributes
        ----------
        colour: str
            the colour of the piece

        pos: Tuple[int, int]
            the position of the piece on the board

        Methods
        -------
        get_colour(self) -> str
            Returns the colour of a piece

        get_pos(self) -> Tuple[int, int]
            Returns the position of a piece

        set_pos(self, pos: Tuple[int, int]) -> None
            Sets the position of a piece

        get_class_name(self) -> str
            Returns the name of the class (for distinction of the inheriting pieces)

        getImage(self) -> pygame.Surface
            returns the image of the piece from the ressources

        move_piece(self, pos: Tuple[int, int]) -> bool
            Tries to move the piece to a given position.
            Returns True if the movement was successfull, else false

        valid_take(self, pos: Tuple[int, int]) -> bool
            Returns if a piece on a given position can be taken or not

        calculate_moves(self, xChange: int, yChange: int = 0) -> List[Tuple[int, int]]
            Calculates all the moves in a given direction and returns them

        pos_reserved(self, pos: Tuple[int, int]) -> bool
            if the position is already reserved by a piece of the same colour or not

        filter_moves(self, moves: List[Tuple[int, int]]) -> List[Tuple[int, int]]
            Filters all the moves for any moves out of the board
            or for any moves which is already occupied by a
            piece of the same colour

        get_moves(self) -> List[Tuple[int, int]]
            Returns all the possible moves for a piece
            (implementation by all the inheriting pieces)
    '''
    def __init__(self, colour: str, pos: Tuple[int, int]) -> None:
        '''
            Parameters
            ----------
            colour: str
                the colour of the piece

            pos: Tuple[int, int]
                the position of the piece on the board
        '''
        self.colour = colour
        self.pos = pos

    def get_colour(self) -> str:
        '''
            Returns the colour of a piece

            Returns
            -------
            str
                the colour of the piece
        '''
        return self.colour

    def get_pos(self) -> Tuple[int, int]:
        '''
            Returns the position of a piece

            Returns
            -------
            Tuple[int, int]
                the position of the piece
        '''
        return self.pos

    def set_pos(self, pos: Tuple[int, int]) -> None:
        '''
            Sets the position of a piece

            Parameters
            ----------
            pos: Tuple[int, int]
                the new position
        '''
        self.pos = pos

    def get_class_name(self) -> str:
        '''
            Returns the name of the class (for distinction of the inheriting pieces)

            Returns
            -------
            str
                the name of the class
        '''
        return self.__class__.__name__

    def getImage(self) -> pygame.Surface:
        '''
            returns the image of the piece from the ressources

            Returns
            -------
            pygame.Surface
                the image of the piece
        '''
        rel_path = '\\sprites\\{}\\{}.png'.format(self.colour, self.get_class_name())
        source_path = Path(__file__).resolve()
        source_dir = source_path.parent
        image = pygame.image.load(source_dir.__str__() + rel_path)
        return pygame.transform.rotozoom(image, 0, 0.45)

    def move_piece(self, pos: Tuple[int, int]) -> bool:
        '''
            Tries to move the piece to a given position.
            Returns True if the movement was successfull, else false

            Parameters
            ----------
            pos: Tuple[int, int]
                the position the piece needs to be moved to

            Returns
            -------
            bool
                is the given position a valid move or not
        '''
        new_pos = next((position for position in self.get_moves() if pos == position), None)
        if new_pos is not None:
            piece_on_new_pos = Piece_Handler.get_piece_on_board(pos)
            if piece_on_new_pos is not None:
                Piece_Handler.remove_piece(piece_on_new_pos)
            self.set_pos(pos)
            Piece_Handler.set_ghost_piece((-1, -1))
            return True
        return False

    def valid_take(self, pos: Tuple[int, int]) -> bool:
        '''
            Returns if a piece on a given position can be taken or not

            Parameters
            ----------
            pos: Tuple[int, int]
                the position of the piece to be taken

            Returns
            -------
            bool
                can the piece be taken or not
        '''
        piece_taken = Piece_Handler.get_piece_on_board(pos)
        return piece_taken is not None and self.colour != piece_taken.colour

    def calculate_moves(self, xChange: int, yChange: int = 0) -> List[Tuple[int, int]]:
        '''
            Calculates all the moves in a given direction and returns them

            Parameters
            ----------
            xChange: int
                the change of the x-coordinate

            yChange: int
                the change of the y-coordinate

            Returns
            -------
            List[Tuple[int, int]]
                All the moves that were calculated
        '''
        moves = []
        i = xChange
        j = yChange
        while Piece_Handler.free_pos((self.pos[0] + i, self.pos[1] + j)):
            moves.append((self.pos[0] + i, self.pos[1] + j))
            i += xChange
            j += yChange
        if self.valid_take((self.pos[0] + i, self.pos[1] + j)):
            moves.append((self.pos[0] + i, self.pos[1] + j))
        return moves

    def pos_reserved(self, pos: Tuple[int, int]) -> bool:
        '''
            Checks if position is already reserved by a piece of the same colour

            Parameters
            ----------
            pos: Tuple[int, int]
                the position of the piece

            Returns
            -------
            bool
                if the position is already reserved by a piece of the same colour or not
        '''
        return not Piece_Handler.free_pos(pos) and Piece_Handler.get_piece_on_board(pos).get_colour() == self.get_colour()

    def filter_moves(self, moves: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        '''
            Filters all the moves for any moves out of the board
            or for any moves which is already occupied by a
            piece of the same colour

            Returns
            -------
            List[Tuple[int, int]]
                all the valid moves the piece
        '''
        moves = Piece_Handler.filter_moves(moves)
        for move in range(moves.__len__() - 1, -1, -1):
            currentMove = moves[move]
            if self.pos_reserved(currentMove):
                moves.remove(moves[move])
        return moves

    @abstractmethod
    def get_moves(self) -> List[Tuple[int, int]]:
        '''
            Returns all the possible moves for a piece
            (implementation by all the child pieces)

            Returns
            -------
            List[Tuple[int, int]]
                all the valid moves
        '''
        pass


class Pawn(Piece):
    '''
        A class for the pawn, which is a child of the Piece-class

        ...

        Attributes
        ----------
        colour: str
            the colour of the piece

        pos: Tuple[int, int]
            the position of the piece on the board

        has_moved: bool
            if the pawn has moved or not

        Methods
        -------
        get_moves(self) -> List[Tuple[int, int]]
            Returns all the possible moves for a piece
            Overrides the method from the Piece-class

        move_piece(self, pos: Tuple[int, int]) -> bool
            Extends the move_piece method from the Piece-class,
            takes into account the en passant move

        Parent
        ------
        Piece
    '''
    def __init__(self, colour: str, pos: Tuple[int, int]) -> None:
        Piece.__init__(self, colour, pos)
        self.has_moved = False

    def get_moves(self) -> List[Tuple[int, int]]:
        '''
            Returns all the possible moves for a piece
            Overrides the method from the Piece-class

            Returns
            -------
            List[Tuple[int, int]]
                all the valid moves
        '''
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
        moves = Piece_Handler.filter_moves(moves)
        return moves

    def move_piece(self, pos: Tuple[int, int]) -> bool:
        '''
            Extends the move_piece method from the Piece-class,
            takes into account the en passant move

            Parameters
            ----------
            pos: Tuple[int, int]
                the position the piece needs to be moved to

            Returns
            -------
            bool
                is the given position a valid move or not
        '''
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
    '''
        A class for the knight, which is a child of the Piece-class

        ...

        Attributes
        ----------
        colour: str
            the colour of the piece

        pos: Tuple[int, int]
            the position of the piece on the board

        Methods
        -------
        get_moves(self) -> List[Tuple[int, int]]
            Returns all the possible moves for a piece
            Overrides the method from the Piece-class

        filter_cartesian(self, moves: List[Tuple[int, int]]) -> List[Tuple[int, int]]
            Filters all the moves out of the cartesian product that don't fit
            into the moving pattern of the knight

        map_moves_to_piece(self, move: Tuple[int, int]) -> Tuple[int, int]
            Maps the filtered cartesian product onto the actual piece

        Parent
        ------
        Piece
    '''
    def get_moves(self) -> List[Tuple[int, int]]:
        '''
            Returns all the possible moves for a piece
            Overrides the method from the Piece-class

            Returns
            -------
            List[Tuple[int, int]]
                all the valid moves
        '''
        cartesian = (-2, -1, 1, 2)
        moves = list(itertools.product(cartesian, cartesian))
        moves = self.filter_cartesian(moves)
        moves = list(map(self.map_moves_to_piece, moves))
        return self.filter_moves(moves)

    def filter_cartesian(self, moves: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        '''
            Filters all the moves out of the cartesian product that don't fit
            into the moving pattern of the knight

            Returns
            -------
            List[Tuple[int, int]]
                all the valid moves for a knight in general
        '''
        for move in range(moves.__len__() - 1, -1, -1):
            currentMove = moves[move]
            if abs(currentMove[0]) == abs(currentMove[1]):
                moves.remove(moves[move])
        return moves

    def map_moves_to_piece(self, move: Tuple[int, int]) -> Tuple[int, int]:
        '''
            Maps the filtered cartesian product onto the actual piece

            Returns
            -------
            List[Tuple[int, int]]
                the valid cartesian moves mapped to the knight
        '''
        x, y = move
        x_self, y_self = self.pos
        return (x + x_self, y + y_self)


class Bishop(Piece):
    '''
        A class for the bishop, which is a child of the Piece-class

        ...

        Attributes
        ----------
        colour: str
            the colour of the piece

        pos: Tuple[int, int]
            the position of the piece on the board

        Methods
        -------
        get_moves(self) -> List[Tuple[int, int]]
            Returns all the possible moves for a piece
            Overrides the method from the Piece-class

        Parent
        ------
        Piece
    '''
    def get_moves(self) -> List[Tuple[int, int]]:
        '''
            Returns all the possible moves for a piece
            Overrides the method from the Piece-class

            Returns
            -------
            List[Tuple[int, int]]
                all the valid moves
        '''
        moves = self.calculate_moves(1, 1)
        moves.extend(self.calculate_moves(-1, 1))
        moves.extend(self.calculate_moves(1, -1))
        moves.extend(self.calculate_moves(-1, -1))
        return moves


class Rook(Piece):
    '''
        A class for the rook, which is a child of the Piece-class

        ...

        Attributes
        ----------
        colour: str
            the colour of the piece

        pos: Tuple[int, int]
            the position of the piece on the board

        has_moved: int
            if the rook has moved or not

        Methods
        -------
        get_moves(self) -> List[Tuple[int, int]]
            Returns all the possible moves for a piece
            Overrides the method from the Piece-class

        get_has_moved(self) -> bool
            Returns if the rook has moved or not

        Parent
        ------
        Piece
    '''
    def __init__(self, colour: str, pos: Tuple[int, int]) -> None:
        Piece.__init__(self, colour, pos)
        self.has_moved = False

    def get_moves(self) -> List[Tuple[int, int]]:
        '''
            Returns all the possible moves for a piece
            Overrides the method from the Piece-class

            Returns
            -------
            List[Tuple[int, int]]
                all the valid moves
        '''
        moves = self.calculate_moves(1)
        moves.extend(self.calculate_moves(-1))
        moves.extend(self.calculate_moves(0, 1))
        moves.extend(self.calculate_moves(0, -1))
        return moves

    def move_piece(self, pos: Tuple[int, int]) -> bool:
        '''
            Extends the move_piece method from the Piece-class,
            takes into account castling

            Parameters
            ----------
            pos: Tuple[int, int]
                the position the piece needs to be moved to

            Returns
            -------
            bool
                is the given position a valid move or not
        '''
        self.has_moved = True
        return super().move_piece(pos)

    def get_has_moved(self) -> bool:
        '''
            Returns if the rook has moved or not

            Returns
            -------
            bool
                if the rook has moved
        '''
        return self.has_moved


class King(Piece):
    '''
        A class for the king, which is a child of the Piece-class

        ...

        Attributes
        ----------
        colour: str
            the colour of the piece

        pos: Tuple[int, int]
            the position of the piece on the board

        has_moved: int
            if the king has moved or not

        Methods
        -------
        get_moves(self) -> List[Tuple[int, int]]
            Returns all the possible moves for a piece
            Overrides the method from the Piece-class

        Parent
        ------
        Piece
    '''
    def __init__(self, colour: str, pos: Tuple[int, int]) -> None:
        Piece.__init__(self, colour, pos)
        self.has_moved = False

    def get_moves(self) -> List[Tuple[int, int]]:
        '''
            Returns all the possible moves for a piece
            Overrides the method from the Piece-class

            Returns
            -------
            List[Tuple[int, int]]
                all the valid moves
        '''
        moves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == 0 and j == 0):
                    moves.append((self.pos[0] + i, self.pos[1] + j))
        if not self.has_moved:
            rook = Piece_Handler.get_piece_on_board((0, self.pos[1]))
            rook.__class__ = Rook
            if rook is not None and not rook.get_has_moved():
                moves.append((self.pos[0] - 2, self.pos[1]))
            rook = Piece_Handler.get_piece_on_board((7, self.pos[1]))
            rook.__class__ = Rook
            if rook is not None and not rook.get_has_moved():
                moves.append((self.pos[0] + 2, self.pos[1]))
        return self.filter_moves(moves)

    def move_piece(self, pos: Tuple[int, int]) -> bool:
        '''
            Extends the move_piece method from the Piece-class,
            takes into account castling

            Parameters
            ----------
            pos: Tuple[int, int]
                the position the piece needs to be moved to

            Returns
            -------
            bool
                is the given position a valid move or not
        '''
        old_pos = self.pos
        successfull = super().move_piece(pos)
        if self.pos[0] - old_pos[0] == 2:
            Piece_Handler.get_piece_on_board((self.pos[0] + 1, self.pos[1])).set_pos((self.pos[0] - 1, self.pos[1]))
        elif self.pos[0] - old_pos[0] == -2:
            Piece_Handler.get_piece_on_board((self.pos[0] - 2, self.pos[1])).set_pos((self.pos[0] + 1, self.pos[1]))
        self.has_moved = True
        return successfull


class Queen(Piece):
    '''
        A class for the queen, which is a child of the Piece-class

        ...

        Attributes
        ----------
        colour: str
            the colour of the piece

        pos: Tuple[int, int]
            the position of the piece on the board

        Methods
        -------
        get_moves(self) -> List[Tuple[int, int]]
            Returns all the possible moves for a piece
            Overrides the method from the Piece-class

        Parent
        ------
        Piece
    '''
    def get_moves(self) -> List[Tuple[int, int]]:
        '''
            Returns all the possible moves for a piece
            Overrides the method from the Piece-class

            Returns
            -------
            List[Tuple[int, int]]
                all the valid moves
        '''
        moves = Rook.get_moves(self)
        moves.extend(Bishop.get_moves(self))
        return moves


class Piece_Handler():
    '''
        A class which handles all the pieces of the game

        ...

        Attributes
        ----------
        pieces: List[Piece]
            all the pieces
        ghost: Tuple[int, int]
            the ghost-position plays an important role for en passant,
            as this is where the position is saved after a pawn moved 2 squares forward

        Methods
        -------
        init_pieces() -> None
            Initializes all the pieces

        get_pieces() -> List[Piece]
            Returns the piece on a given position

        get_piece_on_board(pos: Tuple[int, int]) -> Piece
            Removes a piece from the board

        remove_piece(piece: Piece) -> None
            Removes a piece from the board

        set_ghost_piece(pos: Tuple[int, int]) -> None
            Sets the ghost-position

        get_ghost_piece() -> Tuple[int, int]
            Returns the ghost-position

        filter_moves(moves: List[Tuple[int, int]]) -> List[Tuple[int, int]]
            Filters invalid moves out of a list

        pos_on_board(pos: Tuple[int, int]) -> bool
            Checks if a position is on the board

        free_pos(pos: Tuple[int, int]) -> bool
            Checks if a position is free or not
    '''

    pieces = []
    ghost = (-1, -1)

    @staticmethod
    def init_pieces() -> None:
        '''
            Initializes all the pieces
        '''
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
        '''
            Returns all the pieces

            Returns
            -------
            List[Piece]
                all the pieces
        '''
        return Piece_Handler.pieces

    @staticmethod
    def get_piece_on_board(pos: Tuple[int, int]) -> Piece:
        '''
            Returns the piece on a given position

            Parameters
            ----------
            pos: Tuple[int, int]
                the position

            Returns
            -------
            Piece
                the piece on pos
            None
                if no piece is on the given position
        '''
        return next((piece for piece in Piece_Handler.get_pieces() if piece.get_pos() == pos), None)

    @staticmethod
    def remove_piece(piece: Piece) -> None:
        '''
            Removes a piece from the board

            Parameters
            ----------
            piece: Piece
                the piece that needs to be removed
        '''
        Piece_Handler.pieces.remove(piece)

    @staticmethod
    def set_ghost_piece(pos: Tuple[int, int]) -> None:
        '''
            Sets the ghost-position (important for en passant)

            Parameters
            ----------
            pos: Tuple[int, int]
                the new ghost-position
        '''
        Piece_Handler.ghost = pos

    @staticmethod
    def get_ghost_piece() -> Tuple[int, int]:
        '''
            Returns the ghost-position (important for en passant)

            Returns
            -------
            Tuple[int, int]
                the ghost-position
        '''
        return Piece_Handler.ghost

    @staticmethod
    def filter_moves(moves: List[Tuple[int, int]]) -> List[Tuple[int]]:
        '''
            Filters invalid moves out of a list

            Parameters
            ----------
            moves: List[Tuple[int, int]]
                moves that need to be filtered

            Returns
            -------
            List[Tuple[int, int]]
                all valid moves in the list
        '''
        for move in range(moves.__len__() - 1, -1, -1):
            if not Piece_Handler.pos_on_board(moves[move]):
                moves.remove(moves[move])
        return moves

    @staticmethod
    def pos_on_board(pos: Tuple[int, int]) -> bool:
        '''
            Checks if a position is on the board

            Parameters
            ----------
            pos : Tuple[int, int]
                the position that needs to be checked

            Returns
            -------
            bool
                a boolean if the position is on the board or not
        '''
        return pos[0] >= 0 and pos[0] < 8 and pos[1] >= 0 and pos[1] < 8

    @staticmethod
    def free_pos(pos: Tuple[int, int]) -> bool:
        '''
            Checks if a position is free or not

            Parameters
            ----------
            pos : Tuple[int, int]
                the position that needs to be checked

            Returns
            -------
            bool
                a boolean if the position is free or not
        '''
        return Piece_Handler.pos_on_board(pos) and Piece_Handler.get_piece_on_board(pos) is None
