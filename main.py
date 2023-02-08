import pygame
from objects import *
from typing import Tuple
from sys import exit
from pathlib import Path

pygame.init()
screen = pygame.display.set_mode((800, 750))
screen.fill('mediumseagreen')
pygame.display.set_caption('PyChess')
clock = pygame.time.Clock()
PIECE_SIDE = 70
START_X = 120
START_Y = 100
pieces = []
circles = []
current_piece = None
current_player = 0
boardRectangle = pygame.Rect(START_X, START_Y, 8 * PIECE_SIDE, 8 * PIECE_SIDE)


def load_board():
    is_white = True
    for i in range(8):
        for j in range(8):
            plate = pygame.Surface((PIECE_SIDE, PIECE_SIDE))
            plate.fill('cornsilk' if is_white else 'burlywood4')
            is_white = not is_white
            screen.blit(plate, (START_X + PIECE_SIDE * i, START_Y + PIECE_SIDE * j))
        is_white = not is_white


def drawCircle(pos: Tuple[int, int]):
    rel_path = '\\sprites\\others\\move_circle.png'
    source_path = Path(__file__).resolve()
    source_dir = source_path.parent
    image = pygame.image.load(source_dir.__str__() + rel_path)
    x, y = pos
    x_real = START_X + PIECE_SIDE * x + (PIECE_SIDE - image.get_width()) / 2
    y_real = START_Y + PIECE_SIDE * y + (PIECE_SIDE - image.get_height()) / 2
    screen.blit(image, (x_real, y_real))


def drawCircles():
    for pos in circles:
        drawCircle(pos)


def set_circles(piece: Piece):
    global circles
    circles = piece.get_moves(current_player)


def load_single_piece(piece: Piece):
    image = piece.getImage()
    x, y = piece.get_pos()
    x_real = START_X + PIECE_SIDE * x + (PIECE_SIDE - image.get_width()) / 2
    y_real = START_Y + PIECE_SIDE * y + (PIECE_SIDE - image.get_height()) / 2
    screen.blit(image, (x_real, y_real))


def load_pieces():
    for piece in pieces:
        load_single_piece(piece)


def init_pieces():
    for i in range(8):
        pieces.append(Pawn("white", (i, 6)))
        pieces.append(Pawn("black", (i, 1)))
    pieces.append(Rook("black", (0, 0)))
    pieces.append(Rook("black", (7, 0)))
    pieces.append(Rook("white", (0, 7)))
    pieces.append(Rook("white", (7, 7)))
    pieces.append(Knight("black", (1, 0)))
    pieces.append(Knight("black", (6, 0)))
    pieces.append(Knight("white", (1, 7)))
    pieces.append(Knight("white", (6, 7)))
    pieces.append(Bishop("black", (2, 0)))
    pieces.append(Bishop("black", (5, 0)))
    pieces.append(Bishop("white", (2, 7)))
    pieces.append(Bishop("white", (5, 7)))
    pieces.append(King("black", (4, 0)))
    pieces.append(King("white", (4, 7)))
    pieces.append(Queen("black", (3, 0)))
    pieces.append(Queen("white", (3, 7)))


def get_position(pos: Tuple[int]) -> Tuple[int, int]:
    x, y = pos
    if boardRectangle.collidepoint((x, y)):
        return (int((x - START_X) / PIECE_SIDE), int((y - START_Y) / PIECE_SIDE))
    return (-1, -1)


def get_piece_on_board(pos: Tuple[int]) -> Piece:
    return next((piece for piece in pieces if piece.get_pos() == get_position(pos)), None)


init_pieces()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            piece_clicked = get_piece_on_board(pygame.mouse.get_pos())
            clicked_pos = get_position(pygame.mouse.get_pos())
            if clicked_pos != (-1, -1) and piece_clicked is not None:
                set_circles(get_piece_on_board(pygame.mouse.get_pos()))
                current_piece = piece_clicked
            elif current_piece is not None:
                if current_piece.move_piece(current_player, clicked_pos):
                    circles = []
                    current_player = (current_player + 1) % 2
            else:
                circles = []
    load_board()
    load_pieces()
    drawCircles()
    pygame.display.update()
    clock.tick(60)
