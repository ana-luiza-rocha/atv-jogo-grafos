
import pygame as pg
import sys
import random
from copy import deepcopy

class Bot:
    def __init__(self, my_symbol:str, enemy_symbol:str):
        self.my_symbol = my_symbol
        self.enemy_symbol = enemy_symbol

    def my_move(self, symbol:str|None):
        if symbol == self.my_symbol:
            return True
        return False

    def enemy_move(self, symbol:str|None):
        if not self.my_move(symbol=symbol) and symbol is not None:
            return True
        return False

    def moves_left_in_board(board:list):
        moves = 0
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    moves += 1

        return moves

    def evaluate_board(self, board:list):
        for row in range(3):
            if board[row][0] == board[row][1] and board[row][1] == board[row][2]:
                if self.my_move(board[row][0]):
                    return 10
                if self.enemy_move(board[row][0]):
                    return -10

        for col in range(3):
            if board[0][col] == board[1][col] and board[1][col] == board[2][col]:
                if self.my_move(board[0][col]):
                    return 10
                if self.enemy_move(board[0][col]):
                    return -10

        if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
            if self.my_move(board[0][0]):
                return 10
            if self.enemy_move(board[0][0]):
                return -10

        if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
            if self.my_move(board[0][2]):
                return 10
            if self.enemy_move(board[0][2]):
                return -10

        return 0

    def evaluate_position(self, board:list):

        lines = []

        for row in range(3):
            lines.append(board[row])

        for col in range(3):
            lines.append([board[row][col] for row in range(3)])

        lines.append([board[i][i] for i in range(3)])
        lines.append([board[i][2 - i] for i in range(3)])

        score = 0

        for line in lines:
            my_symbols = line.count(self.my_symbol)
            enemy_symbols = line.count(self.enemy_symbol)

            if enemy_symbols == 0:
                if my_symbols == 1:
                    score += 2
                elif my_symbols == 2:
                    score += 12

            if my_symbols == 0:
                if enemy_symbols == 1:
                    score -= 2
                elif enemy_symbols == 2:
                    score -= 12

        return score

    def get_new_state(self, board:list, move:tuple[int, int], symbol:str, do_copy:bool=False):

        if do_copy:
            board = deepcopy(board)

        row, col = move[0], move[1]

        if board[row][col] is None:
            board[row][col] = symbol

        return board


    def minimax(self, depth, is_max, test_board):

        test_board = deepcopy(test_board)

        score = self.evaluate_board(test_board)

        if score > 0:
            return 100 + depth, None

        if score < 0:
            return -100 + depth, None

        if Bot.moves_left_in_board(test_board) == 0:
            return 0, None

        if depth == 0:
            return self.evaluate_position(test_board), None

        best_move = None

        if is_max:
            best_score = float("-inf")
            current_symbol = self.my_symbol
        else:
            best_score = float("inf")
            current_symbol = self.enemy_symbol

        for i in range(3):
            for j in range(3):

                if test_board[i][j] is None:

                    move = (i, j)

                    next_board = self.get_new_state(
                        board=test_board,
                        move=move,
                        symbol=current_symbol,
                        do_copy=True
                    )

                    # A essência desta recursão remonta ao algoritmo de Depth-First Search

                    score = self.minimax(depth=(depth - 1), is_max=(not is_max), test_board=next_board)[0]

                    if is_max and score > best_score:
                        best_score = score
                        best_move = move

                    elif not is_max and score < best_score:
                        best_score = score
                        best_move = move

        return best_score, best_move

bot = Bot(my_symbol='o', enemy_symbol='x')

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


def draw_home_screen():

    GUI.fill((5, 8, 30))

    # Nebulosas no fundo
    nebula = pg.Surface((width, height + 100), pg.SRCALPHA)
    pg.draw.circle(nebula, (65, 30, 120, 35), (80, 230), 125)
    pg.draw.circle(nebula, (20, 90, 140, 35), (330, 210), 115)
    GUI.blit(nebula, (0, 0))

    # Estrelas
    for x, y, radius, color in stars:
        pg.draw.circle(GUI, color, (x, y), radius)

    # Órbita e planeta
    pg.draw.ellipse(GUI, (145, 105, 255), (85, 205, 230, 65), 2)
    pg.draw.circle(GUI, (40, 105, 190), (200, 235), 55)
    pg.draw.circle(GUI, (80, 165, 220), (182, 218), 17)
    pg.draw.ellipse(GUI, (30, 75, 145), (170, 245, 62, 22))
    pg.draw.ellipse(GUI, (205, 145, 255), (85, 205, 230, 65), 3)

    title_font = pg.font.Font(None, 44)
    title = title_font.render("JOGO DA VELHA", True, (235, 230, 255))
    title_rect = title.get_rect(center=(width / 2, 72))
    GUI.blit(title, title_rect)

    subtitle_font = pg.font.Font(None, 25)
    subtitle = subtitle_font.render("UMA BUSCA POR VIDA EXTRATERRESTRE", True, (160, 190, 230))
    subtitle_rect = subtitle.get_rect(center=(width / 2, 112))
    GUI.blit(subtitle, subtitle_rect)

    button_color = (95, 55, 180)
    if home_button.collidepoint(pg.mouse.get_pos()):
        button_color = (125, 75, 220)

    pg.draw.rect(GUI, button_color, home_button, border_radius=14)
    pg.draw.rect(GUI, (205, 180, 255), home_button, 2, border_radius=14)

    button_font = pg.font.Font(None, 25)
    button_text = button_font.render("PROCURAR VIDA FORA DA TERRA", True, (255, 255, 255))
    button_rect = button_text.get_rect(center=home_button.center)
    GUI.blit(button_text, button_rect)

    hint_font = pg.font.Font(None, 22)
    hint = hint_font.render("UM JOGO DA VELHA ESPACIAL", True, (175, 190, 220))
    hint_rect = hint.get_rect(center=(width / 2, 435))
    GUI.blit(hint, hint_rect)

    pg.display.update()


def draw_planet_map():

    GUI.fill((5, 8, 30))

    # Desenha as estrelas
    for x, y, radius, color in stars:
        pg.draw.circle(GUI, color, (x, y), radius)

    title_font = pg.font.Font(None, 40)
    title = title_font.render("ESCOLHA UM PLANETA", True, (235, 230, 255))
    title_rect = title.get_rect(center=(width / 2, 72))
    GUI.blit(title, title_rect)

    subtitle_font = pg.font.Font(None, 22)
    subtitle = subtitle_font.render("Encontre vida extraterrestre nos planetas",
                                    True, (160, 190, 230))
    subtitle_rect = subtitle.get_rect(center=(width / 2, 112))
    GUI.blit(subtitle, subtitle_rect)

    planet_colors = [(55, 155, 220), (180, 100, 220), (220, 125, 65)]
    planet_labels = ["FASE 1 - FÁCIL", "FASE 2 - MÉDIA", "FASE 3 - DIFÍCIL"]
    mouse_position = pg.mouse.get_pos()
    label_font = pg.font.Font(None, 22)

    for index in range(3):
        planet_button = planet_buttons[index]
        center = planet_button.center
        radius = planet_button.width // 2
        unlocked = index < fases_liberadas

        if unlocked and planet_button.collidepoint(mouse_position):
            pg.draw.circle(GUI, (225, 220, 255), center, radius + 7, 2)

        if unlocked:
            planet_color = planet_colors[index]
            outline_color = (225, 220, 255)
            label_text = planet_labels[index]
            label_color = (220, 220, 245)
        else:
            planet_color = (65, 70, 90)
            outline_color = (115, 120, 140)
            label_text = "BLOQUEADO"
            label_color = (145, 150, 170)

        pg.draw.circle(GUI, planet_color, center, radius)
        pg.draw.circle(GUI, outline_color, center, radius, 2)

        label = label_font.render(label_text, True, label_color)
        label_rect = label.get_rect(center=(center[0], center[1] + radius + 24))
        GUI.blit(label, label_rect)

    hint_font = pg.font.Font(None, 19)
    if fases_liberadas == 1:
        hint_message = "Vença a fase fácil para desbloquear outro planeta"
    elif fases_liberadas == 2:
        hint_message = "Vença a fase média para desbloquear outro planeta"
    else:
        hint_message = "Todas as fases foram liberadas!"
    hint = hint_font.render(hint_message, True, (175, 190, 220))
    hint_rect = hint.get_rect(center=(width / 2, 455))
    GUI.blit(hint, hint_rect)

    pg.display.update()


def draw_result_screen():

    # Tabuleiro final da partida como fundo
    GUI.fill(board_background)

    for line in (1, 2):
        position = int(line * width / 3)
        pg.draw.line(GUI, line_color, (position, 0), (position, height), 7)
        pg.draw.line(GUI, line_color, (0, position), (width, position), 7)

    for row in range(3):
        for col in range(3):
            center_x = int(col * width / 3 + width / 6)
            center_y = int(row * height / 3 + height / 6)

            if board[row][col] == 'x':
                pg.draw.line(GUI, blue, (center_x - 20, center_y - 20),
                             (center_x + 20, center_y + 20), 5)
                pg.draw.line(GUI, blue, (center_x - 20, center_y + 20),
                             (center_x + 20, center_y - 20), 5)
            elif board[row][col] == 'o':
                pg.draw.circle(GUI, orange, (center_x, center_y), 20, 5)

    GUI.fill((11, 18, 48), (0, 400, 400, 100))

    # Camada translúcida para destacar o resultado e os botões
    overlay = pg.Surface((width, height + 100), pg.SRCALPHA)
    overlay.fill((5, 8, 30, 125))
    GUI.blit(overlay, (0, 0))

    if draw:
        result_message = "JOGO EMPATADO!"
    elif winner == 'x':
        result_message = "VOCÊ VENCEU!"
    else:
        result_message = "O BOT VENCEU!"

    result_font = pg.font.Font(None, 42)
    result_text = result_font.render(result_message, True, (235, 230, 255))
    result_rect = result_text.get_rect(center=(width / 2, 58))
    GUI.blit(result_text, result_rect)

    if nivel < 3:
        story_message = "Nenhuma vida encontrada neste planeta."
    elif winner == 'x':
        story_message = "Vida extraterrestre encontrada!"
    else:
        story_message = "A busca continua."

    story_panel = pg.Surface((350, 42), pg.SRCALPHA)
    story_panel.fill((15, 25, 60, 220))
    GUI.blit(story_panel, (25, 91))

    story_font = pg.font.Font(None, 23)
    story_text = story_font.render(story_message, True, (210, 225, 255))
    story_rect = story_text.get_rect(center=(width / 2, 112))
    GUI.blit(story_text, story_rect)

    button_font = pg.font.Font(None, 28)

    has_next_phase = winner == 'x' and nivel < fases_liberadas

    if has_next_phase:
        pg.draw.rect(GUI, (45, 135, 95), next_phase_button, border_radius=12)
        pg.draw.rect(GUI, (165, 235, 195), next_phase_button, 2, border_radius=12)
        next_text = button_font.render("IR PARA A FASE SEGUINTE", True, (255, 255, 255))
        next_rect = next_text.get_rect(center=next_phase_button.center)
        GUI.blit(next_text, next_rect)

    pg.draw.rect(GUI, (95, 55, 180), replay_button, border_radius=12)
    pg.draw.rect(GUI, (205, 180, 255), replay_button, 2, border_radius=12)
    replay_text = button_font.render("JOGAR NOVAMENTE", True, (255, 255, 255))
    replay_rect = replay_text.get_rect(center=replay_button.center)
    GUI.blit(replay_text, replay_rect)

    pg.draw.rect(GUI, (35, 65, 120), map_button, border_radius=12)
    pg.draw.rect(GUI, (150, 190, 255), map_button, 2, border_radius=12)
    map_text = button_font.render("VOLTAR AO MAPA", True, (255, 255, 255))
    map_rect = map_text.get_rect(center=map_button.center)
    GUI.blit(map_text, map_rect)

    pg.display.update()


def draw_status():

    if winner is None:
        message = "Vez do " + XO.upper()
    else:
        message = winner.upper() + " ganhou!"

    if draw:
        message = "Jogo empatado!"

    font = pg.font.Font(None, 30)
    text = font.render(message, 1, (255, 255, 255))

    GUI.fill((11, 18, 48), (0, 400, 400, 100))

    text_rect = text.get_rect(center=(width / 2, 450))
    GUI.blit(text, text_rect)

    level_font = pg.font.Font(None, 24)
    difficulty_names = ["Fácil", "Média", "Difícil"]
    level_text = level_font.render(
        "Dificuldade: " + difficulty_names[nivel - 1],
        1,
        (255, 255, 255)
    )
    level_rect = level_text.get_rect(center=(width / 2, 480))
    GUI.blit(level_text, level_rect)

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

        if winner is None and not draw:
            bot_click()

        draw_status()


def bot_click():

    global XO

    available_moves = [
        (row, col)
        for row in range(3)
        for col in range(3)
        if board[row][col] is None
    ]

    if nivel == 1 or (nivel == 2 and random.random() < 0.7):
        move = random.choice(available_moves)
    else:
        score, move = bot.minimax(
            depth=nivel - 1,
            is_max=True,
            test_board=board
        )

    if move is not None:
        row, col = move
        drawXO(row + 1, col + 1)
        check_win()


def start_game():

    global board, winner, XO, draw, game_started, show_map, result_screen

    XO = 'x'
    winner = None
    draw = False
    board = [[None]*3, [None]*3, [None]*3]
    game_started = True
    show_map = False
    result_screen = False

    GUI.fill(board_background)
    game_initiating_window()


# Inicialização
pg.init()

XO = 'x'
winner = None
draw = False
nivel = 1

width = 400
height = 400

white = (235, 240, 255)
board_background = (8, 14, 40)
orange = (255, 165, 90)
blue = (80, 200, 255)

line_color = (105, 115, 190)

pg.display.set_caption("Jogo da Velha")

GUI = pg.display.set_mode((width, height + 100))
GUI.fill(board_background)

home_button = pg.Rect(40, 340, 320, 62)
next_phase_button = pg.Rect(55, 330, 290, 45)
replay_button = pg.Rect(55, 385, 290, 45)
map_button = pg.Rect(55, 440, 290, 45)
planet_buttons = [
    pg.Rect(48, 208, 72, 72),
    pg.Rect(164, 180, 92, 92),
    pg.Rect(294, 220, 80, 80)
]
stars = [
    (random.randint(5, width - 5), random.randint(5, height + 90),
     random.choice((1, 1, 2)), random.choice(((210, 220, 255), (255, 255, 255), (150, 190, 255))))
    for _ in range(90)
]
game_started = False
show_map = False
result_screen = False
fases_liberadas = 1

board = [[None]*3, [None]*3, [None]*3]

run = True

draw_home_screen()


# Loop principal
while run:

    for event in pg.event.get():

        if event.type == pg.QUIT:
            run = False

        elif event.type == pg.MOUSEBUTTONDOWN:

            if event.button == 1:

                if result_screen:
                    if (winner == 'x' and nivel < fases_liberadas
                            and next_phase_button.collidepoint(event.pos)):
                        nivel += 1
                        start_game()
                    elif replay_button.collidepoint(event.pos):
                        start_game()
                    elif map_button.collidepoint(event.pos):
                        result_screen = False
                        show_map = True
                        draw_planet_map()
                elif game_started:
                    user_click()

                    if winner is not None or draw:
                        if winner == 'x' and nivel == 1:
                            fases_liberadas = max(fases_liberadas, 2)
                        elif winner == 'x' and nivel == 2:
                            fases_liberadas = 3
                        result_screen = True
                        game_started = False
                        draw_result_screen()
                elif not game_started:
                    if show_map:
                        for index, planet_button in enumerate(planet_buttons):
                            if (planet_button.collidepoint(event.pos)
                                    and index + 1 <= fases_liberadas):
                                nivel = index + 1
                                start_game()
                                break
                    elif home_button.collidepoint(event.pos):
                        show_map = True
                        draw_planet_map()

    if result_screen:
        draw_result_screen()
    elif game_started:
        pg.display.update()
    elif show_map:
        draw_planet_map()
    else:
        draw_home_screen()


pg.quit()
sys.exit()

