import pygame
from objects import *
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 750))
screen.fill('mediumseagreen')
pygame.display.set_caption('PyChess')
clock = pygame.time.Clock()
PIECE_SIDE = 70
pieces = []


def load_board():
    is_white = True
    for i in range(8):
        for j in range(8):
            plate = pygame.Surface((PIECE_SIDE, PIECE_SIDE))
            plate.fill('cornsilk' if is_white else 'burlywood4')
            is_white = not is_white
            screen.blit(plate, (120 + PIECE_SIDE * i, 100 + PIECE_SIDE * j))
        is_white = not is_white


def load_single_piece(piece: Piece):
    image = piece.getImage()
    x, y = piece.get_pos()
    x_real = 120 + PIECE_SIDE * x + (PIECE_SIDE - image.get_width()) / 2
    y_real = 100 + PIECE_SIDE * y + (PIECE_SIDE - image.get_height()) / 2
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


init_pieces()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    load_board()
    load_pieces()
    pygame.display.update()
    clock.tick(60)
