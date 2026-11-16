import random
from bot import Bot

class Game:
    def __init__(self, board:list, player_XO:str="x", bot_XO:str="o", bot_difficulty:int=3, steps_offset:int=random.randint(0, 1)):
        self.board = board
        self.bot_difficulty = bot_difficulty

        self.bot_XO = bot_XO
        self.player_XO = player_XO

        self.bot = Bot(bot_XO, player_XO)

        self.steps = steps_offset

        self.winner = None
        self.draw = False

    def get_turn(self):

        # player turn = 0
        # bot turn = 1

        return self.steps % 2

    def is_move_legal(self, row:int, col:int):
        return self.board[row][col] is None

    def apply_move(self, row:int, col:int, XO:str):
        if self.is_move_legal(row=row, col=col):
            self.board[row][col] = XO
        else:
            print("Location not empty.")

    def bot_play(self):
        move = self.bot.get_move(depth=self.bot_difficulty, board=self.board)
        self.apply_move(move[0], move[1], self.bot_XO)

    def update_winner(self):
        # Verificando linhas
        for row in range(3):

            if (self.board[row][0] == self.board[row][1] == self.board[row][2]
                    and self.board[row][0] is not None):

                self.winner = self.board[row][0]
                return

        # Verificando colunas
        for col in range(3):

            if (self.board[0][col] == self.board[1][col] == self.board[2][col]
                    and self.board[0][col] is not None):

                self.winner = self.board[0][col]
                return

        # Diagonal principal
        if (self.board[0][0] == self.board[1][1] == self.board[2][2]
                and self.board[0][0] is not None):

            self.winner = self.board[0][0]
            return

        # Diagonal secundária
        if (self.board[0][2] == self.board[1][1] == self.board[2][0]
                and self.board[0][2] is not None):

            self.winner = self.board[0][2]
            return

        # Verificando empate
        if all(self.board[row][col] is not None
            for row in range(3) for col in range(3)):

            self.draw = True
