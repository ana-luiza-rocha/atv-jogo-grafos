import random
import pygame as pg
import time

from game import Game
from interface import GameScreen

def quitting_check(speficic_event=None):
    if speficic_event is None:
        for event in (pg.event.get()):
            if event.type == pg.QUIT:
                return True
    else:
        if speficic_event.type == pg.QUIT:
            return True
        
    return False

def begin_round():

    player_XO = "x"
    bot_XO = "o"

    bot_difficulty = 10
    steps_offset = random.randint(0, 1)

    board = [ [None] * 3, [None] * 3 , [None] * 3 ]

    game = Game(board=board, player_XO=player_XO, bot_XO=bot_XO, bot_difficulty=bot_difficulty, steps_offset=steps_offset)

    game_screen = GameScreen(board=board, player_XO=player_XO, bot_XO=bot_XO)

    quitted = False

    while not game.winner and not game.draw and not quitted:

        game_screen.update_draw_board()

        turn = game.get_turn()

        XO = player_XO if turn == 0 else bot_XO

        game_screen.draw_status(winner=game.winner, XO= XO)

        if turn == 0:

            game_screen.interactable = True

            finished_turn = False
            
            while not finished_turn:

                for event in (pg.event.get()):

                    quitted = quitting_check(event)

                    if not quitted and event.type == pg.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            move = game_screen.user_click()
                            if move is not None and game.is_move_legal(row=move[0], col=move[1]):
                                game.apply_move(row=move[0], col=move[1], XO=XO)
                                finished_turn = True

                pg.display.update()


        else:

            game_screen.interactable = False

            begin_time = time.time()
            wait_time = random.random() * 0.5 + 0.3

            while (time.time() - begin_time < wait_time):
                pg.display.update()
                quitted = quitting_check()

            game.bot_play()

        pg.display.update()

        game.update_winner()

        game.steps += 1

    after_game_run = True

    while after_game_run:
        pg.display.update()
        after_game_run = quitting_check()

begin_round()