from bot import Bot
import random
from time import sleep as wait
from tabulate import tabulate

player1_symbol = "x"
player2_symbol = "o"

board = [ [None] * 3, [None] * 3 , [None] * 3 ]

bot1 = Bot(player1_symbol, player2_symbol)
bot2 = Bot(player2_symbol, player1_symbol)

bots = [bot1, bot2]

steps = 0

def print_board():
    show = tabulate(board, tablefmt="grid")

    print(show)

offset = random.randint(0, 1)

while True:

    turn_index = (steps + offset ) % 2

    turn_bot:Bot = bots [ turn_index ]

    result = turn_bot.minimax(depth=30, is_max=(turn_index == 0), test_board=board)

    move = result[1]

    if move is None:
        print("Jogo acabou!")
        break

    board[move[0]][move[1]] = turn_bot.my_symbol

    print_board()
    print(result[0])

    steps += 1

    wait(1)
