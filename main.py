import pygame
from objects import Piece_Handler, Piece
from typing import Tuple
from sys import exit
from pathlib import Path
from enum import Enum

pygame.init()
X = 800
Y = 750
screen = pygame.display.set_mode((X, Y))
screen.fill('mediumseagreen')
pygame.display.set_caption('PyChess')
clock = pygame.time.Clock()
PIECE_SIDE = 70
START_X = 120
START_Y = 100
circles = []
current_piece = None
current_player = 0
promotion_screen_active = False
boardRectangle = pygame.Rect(START_X, START_Y, 8 * PIECE_SIDE, 8 * PIECE_SIDE)
GameState = Enum('GameState', ['MENUE', 'RUNNING', 'GAMEOVER'])
state = GameState.MENUE
btnRect = None


def load_board() -> None:
    '''
        Draws the board on the window
    '''
    is_white = True
    for i in range(8):
        for j in range(8):
            plate = pygame.Surface((PIECE_SIDE, PIECE_SIDE))
            plate.fill('cornsilk' if is_white else 'burlywood4')
            is_white = not is_white
            screen.blit(plate, (START_X + PIECE_SIDE * i, START_Y + PIECE_SIDE * j))
        is_white = not is_white


def drawCircle(pos: Tuple[int, int]) -> None:
    '''
        Draws the circle on a given position

        Parameters
        ----------
        pos: Tuple[int, int]
            the position of the circle where it needs to be drawn
    '''
    if Piece_Handler.get_piece_on_board(pos) is None and (pos != Piece_Handler.get_ghost_piece() or current_piece.get_class_name() != "Pawn"):
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


def drawCircles() -> None:
    '''
        draws all the circles on the board for where the selected piece can move
    '''
    for pos in circles:
        drawCircle(pos)


def set_circles(piece: Piece) -> None:
    '''
        Sets the circles variable to the possible moves of the selected piece

        Parameters
        ----------
        piece: Piece
            the piece from which the moves need to be saved
    '''
    global circles
    circles = piece.get_moves()


def load_single_piece(piece: Piece) -> None:
    '''
        Draws a piece on the board

        Parameters
        ----------
        piece: Piece
            The piece that needs to be drawn on the board
    '''
    image = piece.getImage()
    x, y = piece.get_pos()
    x_real = START_X + PIECE_SIDE * x + (PIECE_SIDE - image.get_width()) / 2
    y_real = START_Y + PIECE_SIDE * y + (PIECE_SIDE - image.get_height()) / 2
    screen.blit(image, (x_real, y_real))


def load_pieces() -> None:
    '''
        Loads all the pieces to the board
    '''
    for piece in Piece_Handler.get_pieces():
        load_single_piece(piece)


def get_position(pos: Tuple[int, int]) -> Tuple[int, int]:
    '''
        Turns the coordinates of the mouse-click into a position on the board
        and returns it

        Parameters
        ----------
        pos: Tuple[int, int]
            the mouse-coordinates

        Returns
        -------
        Tuple[int, int]
            the board-coordinates the mouse clicked
    '''
    x, y = pos
    if boardRectangle.collidepoint((x, y)):
        return (int((x - START_X) / PIECE_SIDE), int((y - START_Y) / PIECE_SIDE))
    return (-1, -1)


def get_promotion_position(mouse_pos: Tuple[int, int]) -> Tuple[int, int]:
    '''
        Turns the coordinates of the mouse-click into a position on the promotion-screen
        and returns it

        Parameters
        ----------
        mouse_pos: Tuple[int, int]
            the mouse-coordinates

        Returns
        -------
        Tuple[int, int]
            the promotion-coordinates the mouse clicked
    '''
    board_pos = get_position(mouse_pos)
    x, y = (board_pos[0] - 3, board_pos[0] - 3)
    if x >= 0 and x <= 1 and y >= 0 and y <= 1:
        return (x, y)
    else:
        return (-1, -1)


def draw_promotion_screen() -> None:
    '''
        Draws the promotion-screen on the board
    '''
    promotion = pygame.Surface((PIECE_SIDE * 2, PIECE_SIDE * 2))
    promotion.fill("white")
    screen.blit(promotion, (START_X + PIECE_SIDE * 3, START_Y + PIECE_SIDE * 3))
    draw_promotion_pieces()


def draw_promotion_piece(colour: str, piece: str, pos: Tuple[int, int]) -> None:
    '''
        Draws a single piece on the promotion screen

        Parameters
        ----------
        colour: str
            the colour of the piece

        piece: str
            the name of the piece

        pos: Tuple[int, int]
            where the piece is located on the promotion-screen
    '''
    rel_path = '\\sprites\\{}\\{}.png'.format(colour, piece)
    source_path = Path(__file__).resolve()
    source_dir = source_path.parent
    image = pygame.image.load(source_dir.__str__() + rel_path)
    image = pygame.transform.rotozoom(image, 0, 0.45)
    x = pos[0] + 3
    y = pos[1] + 3
    x_real = START_X + PIECE_SIDE * x + (PIECE_SIDE - image.get_width()) / 2
    y_real = START_Y + PIECE_SIDE * y + (PIECE_SIDE - image.get_height()) / 2
    screen.blit(image, (x_real, y_real))


def draw_promotion_pieces() -> None:
    '''
        Draws all the promotion pieces onto the promotion screen
    '''
    draw_promotion_piece(current_piece.get_colour(), "queen", (0, 0))
    draw_promotion_piece(current_piece.get_colour(), "knight", (0, 1))
    draw_promotion_piece(current_piece.get_colour(), "bishop", (1, 0))
    draw_promotion_piece(current_piece.get_colour(), "rook", (1, 1))


def get_promotion(pos: Tuple[int, int]) -> str:
    '''
        Turns a given position on the promotion screen to the
        respective piece

        Parameters
        ----------
        pos: Tuple[int, int]
            the position on the promotion-screen
    '''
    match pos:
        case (0, 0):
            return "queen"
        case (0, 1):
            return "knight"
        case (1, 0):
            return "bishop"
        case (1, 1):
            return "rook"


def is_promotion_ready() -> bool:
    '''
        Checks if a pawn needs to be promoted or not
    '''
    return current_piece.get_class_name() == "Pawn" and (current_piece.get_pos()[1] == 0 or current_piece.get_pos()[1] == 7)


def draw_screen(string: str) -> None:
    '''
        Draws the menue and gameOver-screen to the window

        Parameters
        ----------
        string: str
            The title string
    '''
    global btnRect
    titleFont = pygame.font.Font("freesansbold.ttf", 60)
    title = titleFont.render(string, True, (0, 0, 0))
    titleRect = title.get_rect()
    titleRect.center = (X // 2, 150)
    screen.blit(title, titleRect)
    btnFont = pygame.font.Font("freesansbold.ttf", 45)
    btn = btnFont.render("Play", True, (0, 0, 0))
    btnRect = btn.get_rect()
    btnRect.center = (X // 2, 400)
    btnRectCpy = btnRect.copy()
    btnRectCpy.inflate_ip(30, 30)
    pygame.draw.rect(screen, (0, 0, 0), btnRectCpy, 3)
    screen.blit(btn, btnRect)


def draw_menue() -> None:
    '''
        Draws the menue to the window
    '''
    draw_screen("PyChess")


def draw_game() -> None:
    '''
        Draws the game to the window
    '''
    load_board()
    load_pieces()
    drawCircles()
    if promotion_screen_active:
        draw_promotion_screen()


def click_on_menue() -> None:
    '''
        Checks if the player clickes on the play button
    '''
    global btnRect, state, circles, current_player
    pos = pygame.mouse.get_pos()
    if (btnRect.collidepoint(pos)):
        state = GameState.RUNNING
        Piece_Handler.init_pieces()
        circles = []
        current_player = 0


def draw_gameover() -> None:
    '''
        Draws the gameOver-screen to the window
    '''
    global current_player
    if current_player == 0:
        draw_screen("White has won")
    else:
        draw_screen("Black has won")


def run_game() -> None:
    '''
        Runs the game and contains all the chess-logic
    '''
    global promotion_screen_active, current_piece, circles, current_player, state
    if promotion_screen_active:
        pos = get_promotion_position(pygame.mouse.get_pos())
        if pos != (-1, -1):
            promotion_piece = get_promotion(pos)
            Piece_Handler.promote_piece(current_piece, promotion_piece)
            current_piece = None
            promotion_screen_active = False
    else:
        clicked_pos = get_position(pygame.mouse.get_pos())
        piece_clicked = Piece_Handler.get_piece_on_board(clicked_pos)
        if clicked_pos != (-1, -1) and piece_clicked is not None and current_piece is None:
            white_turn = current_player == 0 and piece_clicked.get_colour() == "white"
            black_turn = current_player == 1 and piece_clicked.get_colour() == "black"
            if white_turn or black_turn:
                set_circles(Piece_Handler.get_piece_on_board(clicked_pos))
                current_piece = piece_clicked
        elif current_piece is not None and clicked_pos != (-1, -1) and clicked_pos in circles:
            clicked_piece = Piece_Handler.get_piece_on_board(clicked_pos)
            if clicked_piece is not None and clicked_piece.get_class_name() == "King":
                state = GameState.GAMEOVER
                screen.fill("mediumseagreen")
            elif current_piece.move_piece(clicked_pos):
                circles = []
                current_player = (current_player + 1) % 2
                if is_promotion_ready():
                    promotion_screen_active = True
                else:
                    current_piece = None
        else:
            circles = []
            current_piece = None


if __name__ == "__main__":
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                match state:
                    case GameState.MENUE | GameState.GAMEOVER:
                        click_on_menue()
                    case GameState.RUNNING:
                        run_game()
        match state:
            case GameState.MENUE:
                draw_menue()
            case GameState.RUNNING:
                draw_game()
            case GameState.GAMEOVER:
                draw_gameover()
        pygame.display.update()
        clock.tick(60)
