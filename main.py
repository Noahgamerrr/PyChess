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
circles = []
current_piece = None
current_player = 0
boardRectangle = pygame.Rect(START_X, START_Y, 8 * PIECE_SIDE, 8 * PIECE_SIDE)
Piece_Handler.init_pieces()


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
    if Piece_Handler.get_piece_on_board(pos) is None:
        rel_path = '\\sprites\\others\\move_circle.png'
    else:
        rel_path = '\\sprites\\others\\take_circle.png'
    source_path = Path(__file__).resolve()
    source_dir = source_path.parent
    image = pygame.image.load(source_dir.__str__() + rel_path)
    x, y = pos
    x_real = START_X + PIECE_SIDE * x + (PIECE_SIDE - image.get_width()) / 2
    y_real = START_Y + PIECE_SIDE * y + (PIECE_SIDE - image.get_height()) / 2
    image.set_alpha(100)
    screen.blit(image, (x_real, y_real))


def drawCircles():
    for pos in circles:
        drawCircle(pos)


def set_circles(piece: Piece):
    global circles
    circles = piece.get_moves()


def load_single_piece(piece: Piece):
    image = piece.getImage()
    x, y = piece.get_pos()
    x_real = START_X + PIECE_SIDE * x + (PIECE_SIDE - image.get_width()) / 2
    y_real = START_Y + PIECE_SIDE * y + (PIECE_SIDE - image.get_height()) / 2
    screen.blit(image, (x_real, y_real))


def load_pieces():
    for piece in Piece_Handler.get_pieces():
        load_single_piece(piece)


def get_position(pos: Tuple[int]) -> Tuple[int, int]:
    x, y = pos
    if boardRectangle.collidepoint((x, y)):
        return (int((x - START_X) / PIECE_SIDE), int((y - START_Y) / PIECE_SIDE))
    return (-1, -1)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked_pos = get_position(pygame.mouse.get_pos())
            piece_clicked = Piece_Handler.get_piece_on_board(clicked_pos)
            if current_piece is not None:
                if current_piece.move_piece(clicked_pos):
                    circles = []
                    current_player = (current_player + 1) % 2
                    current_piece = None
            elif clicked_pos != (-1, -1) and piece_clicked is not None:
                white_turn = current_player == 0 and piece_clicked.get_colour() == "white"
                black_turn = current_player == 1 and piece_clicked.get_colour() == "black"
                if white_turn or black_turn:
                    set_circles(Piece_Handler.get_piece_on_board(clicked_pos))
                    current_piece = piece_clicked
            else:
                circles = []
                current_piece = None
    load_board()
    load_pieces()
    drawCircles()
    pygame.display.update()
    clock.tick(60)
