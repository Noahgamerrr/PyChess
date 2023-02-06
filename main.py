import pygame
from sys import exit
from pathlib import Path

pygame.init()
screen = pygame.display.set_mode((800, 750))
screen.fill('mediumseagreen')
pygame.display.set_caption('PyChess')
clock = pygame.time.Clock()
PIECE_SIDE = 70
pieces = ["king", "pawn", "knight", "bishop", "rook", "queen"]
board = [
    [10, 8, 9, 11, 12, 9, 8, 10],
    [7, 7, 7, 7, 7, 7, 7, 7],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [4, 2, 3, 5, 6, 3, 2, 4]
]


def loadBoard():
    isWhite = True
    for i in range(8):
        for j in range(8):
            plate = pygame.Surface((PIECE_SIDE, PIECE_SIDE))
            plate.fill('cornsilk' if isWhite else 'burlywood4')
            isWhite = not isWhite
            screen.blit(plate, (120 + PIECE_SIDE * i, 100 + PIECE_SIDE * j))
        isWhite = not isWhite


def loadSinglePiece(colour, piece, pos):
    rel_path = '\\sprites\\{}\\{}.png'.format(colour, piece)
    source_path = Path(__file__).resolve()
    source_dir = source_path.parent
    piece = pygame.image.load(source_dir.__str__() + rel_path)
    piece = pygame.transform.rotozoom(piece, 0, 0.45)
    x, y = pos
    xReal = 120 + PIECE_SIDE * x + (PIECE_SIDE - piece.get_width()) / 2
    yReal = 100 + PIECE_SIDE * y + (PIECE_SIDE - piece.get_height()) / 2
    screen.blit(piece, (xReal, yReal))


def loadPieces():
    for rows in range(board.__len__()):
        for columns in range(board[rows].__len__()):
            if board[rows][columns] == 0:
                continue
            colour = 'white' if board[rows][columns] <= 6 else 'black'
            piece = board[rows][columns] % 6
            loadSinglePiece(colour, pieces[piece], (columns, rows))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    loadBoard()
    loadPieces()
    pygame.display.update()
    clock.tick(60)
