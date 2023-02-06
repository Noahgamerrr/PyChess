import pygame
from sys import exit
from pathlib import Path

pygame.init()
screen = pygame.display.set_mode((800, 750))
screen.fill('mediumseagreen')
pygame.display.set_caption('PyChess')
clock = pygame.time.Clock()


def loadBoard():
    isWhite = True
    for i in range(8):
        for j in range(8):
            plate = pygame.Surface((70, 70))
            plate.fill('cornsilk' if isWhite else 'burlywood4')
            isWhite = not isWhite
            screen.blit(plate, (120 + 70 * i, 100 + 70 * j))
        isWhite = not isWhite


def loadSinglePiece(colour, piece):
    rel_path = '\\sprites\\{}\\{}.png'.format(colour, piece)
    source_path = Path(__file__).resolve()
    source_dir = source_path.parent
    piece = pygame.image.load(source_dir.__str__() + rel_path)
    return pygame.transform.rotozoom(piece, 0, 0.45)


def loadPieces():
    curr_piece = loadSinglePiece('white', 'pawn')
    for i in range(8):
        screen.blit(curr_piece, (131 + 70 * i, 528))
    curr_piece = loadSinglePiece('white', 'rook')
    screen.blit(curr_piece, (128, 600))
    screen.blit(curr_piece, (618, 600))
    curr_piece = loadSinglePiece('white', 'knight')
    screen.blit(curr_piece, (198, 600))
    screen.blit(curr_piece, (548, 600))
    curr_piece = loadSinglePiece('white', 'bishop')
    screen.blit(curr_piece, (266, 600))
    screen.blit(curr_piece, (476, 600))
    curr_piece = loadSinglePiece('white', 'queen')
    screen.blit(curr_piece, (333, 600))
    curr_piece = loadSinglePiece('white', 'king')
    screen.blit(curr_piece, (405, 600))
    curr_piece = loadSinglePiece('black', 'pawn')
    for i in range(8):
        screen.blit(curr_piece, (131 + 70 * i, 180))
    curr_piece = loadSinglePiece('black', 'rook')
    screen.blit(curr_piece, (128, 110))
    screen.blit(curr_piece, (618, 110))
    curr_piece = loadSinglePiece('black', 'knight')
    screen.blit(curr_piece, (198, 110))
    screen.blit(curr_piece, (548, 110))
    curr_piece = loadSinglePiece('black', 'bishop')
    screen.blit(curr_piece, (266, 110))
    screen.blit(curr_piece, (476, 110))
    curr_piece = loadSinglePiece('black', 'queen')
    screen.blit(curr_piece, (333, 110))
    curr_piece = loadSinglePiece('black', 'king')
    screen.blit(curr_piece, (405, 110))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    loadBoard()
    loadPieces()
    pygame.display.update()
    clock.tick(60)
