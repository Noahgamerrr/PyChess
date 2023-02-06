import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 750))
screen.fill('mediumseagreen')
pygame.display.set_caption('PyChess')
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    isWhite = True
    for i in range(8):
        for j in range(8):
            plate = pygame.Surface((70, 70))
            plate.fill('cornsilk' if isWhite else 'burlywood4')
            isWhite = not isWhite
            screen.blit(plate, (120 + 70 * i, 100 + 70 * j))
        isWhite = not isWhite
    pygame.display.update()
    clock.tick(60)
