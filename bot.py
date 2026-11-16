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

        if score != 0:
            return score, None

        if Bot.moves_left_in_board(test_board) == 0 or depth == 0:
            return 0, None

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

                    next_board = self.get_new_state(board=test_board, move=move, symbol=current_symbol)

                    # A essência desta recursão remonta ao algoritmo de Depth-First Search

                    score = self.minimax(depth=(depth - 1), is_max=(not is_max), test_board=next_board)[0]

                    if is_max and score > best_score:
                        best_score = score
                        best_move = move

                    elif not is_max and score < best_score:
                        best_score = score
                        best_move = move

        return best_score, best_move

    def get_move(self, depth:int, board:list) -> tuple[int, int]:
        return self.minimax(depth=depth, is_max=True, test_board=board)[1]