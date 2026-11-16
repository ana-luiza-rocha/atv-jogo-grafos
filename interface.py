
import pygame as pg
import sys

def game_initiating_window():

    # Linhas verticais
    pg.draw.line(GUI, line_color, (width / 3, 0),
                 (width / 3, height), 7)

    pg.draw.line(GUI, line_color, (width / 3 * 2, 0),
                 (width / 3 * 2, height), 7)

    # Linhas horizontais
    pg.draw.line(GUI, line_color, (0, height / 3),
                 (width, height / 3), 7)

    pg.draw.line(GUI, line_color, (0, height / 3 * 2),
                 (width, height / 3 * 2), 7)

    draw_status()


def draw_status():

    if winner is None:
        message = "Vez do " + XO.upper()
    else:
        message = winner.upper() + " ganhou!"

    if draw:
        message = "Jogo empatado!"

    font = pg.font.Font(None, 30)
    text = font.render(message, 1, (255, 255, 255))

    GUI.fill((0, 0, 0), (0, 400, 400, 100))

    text_rect = text.get_rect(center=(width / 2, 450))
    GUI.blit(text, text_rect)

    pg.display.update()


def drawXO(row, col):

    global board, XO

    # Centro do quadrante
    posx = int((col - 1) * (width / 3) + (width / 6))
    posy = int((row - 1) * (height / 3) + (height / 6))

    board[row-1][col-1] = XO

    if XO == 'x':

        # X azul
        pg.draw.line(GUI, blue,
                     (posx - 20, posy - 20),
                     (posx + 20, posy + 20), 5)

        pg.draw.line(GUI, blue,
                     (posx - 20, posy + 20),
                     (posx + 20, posy - 20), 5)

        XO = 'o'

    else:

        # O laranja
        pg.draw.circle(GUI, orange, (posx, posy), 20, 5)

        XO = 'x'

    pg.display.update()


def check_win():

    global winner, draw

    # Verificando linhas
    for row in range(3):

        if (board[row][0] == board[row][1] == board[row][2]
                and board[row][0] is not None):

            winner = board[row][0]
            return

    # Verificando colunas
    for col in range(3):

        if (board[0][col] == board[1][col] == board[2][col]
                and board[0][col] is not None):

            winner = board[0][col]
            return

    # Diagonal principal
    if (board[0][0] == board[1][1] == board[2][2]
            and board[0][0] is not None):

        winner = board[0][0]
        return

    # Diagonal secundária
    if (board[0][2] == board[1][1] == board[2][0]
            and board[0][2] is not None):

        winner = board[0][2]
        return

    # Verificando empate
    if all(board[row][col] is not None
           for row in range(3) for col in range(3)):

        draw = True


def user_click():

    if winner is not None or draw:
        return

    x, y = pg.mouse.get_pos()

    # Coluna
    if x < width / 3:
        col = 1
    elif x < width / 3 * 2:
        col = 2
    elif x < width:
        col = 3
    else:
        col = None

    # Linha
    if y < height / 3:
        row = 1
    elif y < height / 3 * 2:
        row = 2
    elif y < height:
        row = 3
    else:
        row = None

    if row and col and board[row-1][col-1] is None:

        drawXO(row, col)

        check_win()

        draw_status()


def reset_game():

    global board, winner, XO, draw

    pg.time.delay(3000)

    XO = 'x'
    winner = None
    draw = False

    board = [[None]*3, [None]*3, [None]*3]

    GUI.fill(white)
    game_initiating_window()


# Inicialização
pg.init()

XO = 'x'
winner = None
draw = False

width = 400
height = 400

white = (255, 255, 255)
orange = (255, 165, 0)
blue = (0, 0, 255)

line_color = (0, 0, 0)

pg.display.set_caption("Jogo da Velha")

GUI = pg.display.set_mode((width, height + 100))
GUI.fill(white)

board = [[None]*3, [None]*3, [None]*3]

run = True

game_initiating_window()


# Loop principal
while run:

    for event in pg.event.get():

        if event.type == pg.QUIT:
            run = False

        elif event.type == pg.MOUSEBUTTONDOWN:

            if event.button == 1:

                user_click()

                if winner is not None or draw:
                    reset_game()

    pg.display.update()


pg.quit()
sys.exit()
