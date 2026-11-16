
import pygame as pg
import sys

white = (255, 255, 255)
orange = (255, 165, 0)
blue = (0, 0, 255)

line_color = (0, 0, 0)

class GameScreen:

    def __init__(self, board, player_XO="x", bot_XO="o", width=400, height=400):
        pg.init()

        self.board = board # if board is not None else [[None]*3, [None]*3, [None]*3]
        self.width = width
        self.height = height
        self.winner = None
        self.draw = False

        self.interactable = True

        self.player_XO = player_XO
        self.bot_XO = bot_XO

        self.drawn_coordinates = []

        pg.display.set_caption("Jogo da Velha")

        self.GUI = pg.display.set_mode((width, height + 100))
        self.GUI.fill(white)

        self.game_initiating_window()

    def game_initiating_window(self):

        # Linhas verticais
        pg.draw.line(self.GUI, line_color, (self.width / 3, 0),
                    (self.width / 3, self.height), 7)

        pg.draw.line(self.GUI, line_color, (self.width / 3 * 2, 0),
                    (self.width / 3 * 2, self.height), 7)

        # Linhas horizontais
        pg.draw.line(self.GUI, line_color, (0, self.height / 3),
                    (self.width, self.height / 3), 7)

        pg.draw.line(self.GUI, line_color, (0, self.height / 3 * 2),
                    (self.width, self.height / 3 * 2), 7)

    def draw_status(self, winner:str|None, XO:str):

        if self.winner is None:
            message = "Vez do " + XO.upper()
        else:
            message = winner.upper() + " ganhou!"

        if self.draw:
            message = "Jogo empatado!"

        font = pg.font.Font(None, 30)
        text = font.render(message, 1, (255, 255, 255))

        self.GUI.fill((0, 0, 0), (0, 400, 400, 100))

        text_rect = text.get_rect(center=(self.width / 2, 450))
        self.GUI.blit(text, text_rect)

        pg.display.update()

    def drawXO(self, row, col, XO):

        # Centro do quadrante
        posx = int((col) * (self.width / 3) + (self.width / 6))
        posy = int((row) * (self.height / 3) + (self.height / 6))

        self.board[row][col] = XO
        self.drawn_coordinates.append((row, col))

        if XO == 'x':

            # X azul
            pg.draw.line(self.GUI, blue,
                        (posx - 20, posy - 20),
                        (posx + 20, posy + 20), 5)

            pg.draw.line(self.GUI, blue,
                        (posx - 20, posy + 20),
                        (posx + 20, posy - 20), 5)

            # XO = 'o'

        else:

            # O laranja
            pg.draw.circle(self.GUI, orange, (posx, posy), 20, 5)

            # XO = 'x'

        pg.display.update()

    def update_draw_board(self):
        for row in range(3):
            for col in range(3):

                if (row, col) in self.drawn_coordinates:
                    continue

                if self.board[row][col] is None:
                    continue

                XO = self.board[row][col]

                self.drawXO(row=row, col=col, XO=XO)

    def user_click(self):

        if self.interactable == False:
            return

        x, y = pg.mouse.get_pos()

        # Coluna
        if x < self.width / 3:
            col = 0
        elif x < (self.width / 3) * 2:
            col = 1
        elif x < self.width:
            col = 2
        else:
            col = None

        # Linha
        if y < self.height / 3:
            row = 0
        elif y < (self.height / 3) * 2:
            row = 1
        elif y < self.height:
            row = 2
        else:
            row = None

        if row is not None and col is not None and self.board[row][col] is None:
            return (row, col)
        else:
            print(self.board[row][col])
            return ("cook", "strogonoff")

    # def reset_game(self):
    #     pg.time.delay(3000)

    #     # self.XO = 'x'
    #     self.winner = None
    #     self.draw = False

    #     self.board = [[None]*3, [None]*3, [None]*3]

    #     GUI.fill(white)
    #     self.game_initiating_window()

# Inicialização
# pg.init()

# XO = 'x'
# winner = None
# draw = False

# width = 400
# height = 400

# white = (255, 255, 255)
# orange = (255, 165, 0)
# blue = (0, 0, 255)

# line_color = (0, 0, 0)

# pg.display.set_caption("Jogo da Velha")

# GUI = pg.display.set_mode((width, height + 100))
# GUI.fill(white)

# board = [[None]*3, [None]*3, [None]*3]

# run = True

# game_initiating_window()


# # Loop principal
# while run:

#     for event in pg.event.get():

#         if event.type == pg.QUIT:
#             run = False

#         elif event.type == pg.MOUSEBUTTONDOWN:

#             if event.button == 1:

#                 user_click()

#                 if winner is not None or draw:
#                     reset_game()

#     pg.display.update()


# pg.quit()
# sys.exit()
