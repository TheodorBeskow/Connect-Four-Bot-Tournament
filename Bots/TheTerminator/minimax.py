from connect4 import Connect4
import random

INF = 1000000
PLAYER_PIECE = 1
OPPONENT_PIECE = 2

class Bot:
    def __init__(self):
        self.board = None
        self.bestMove = None
        self.startTime = None

    def choose_move(self, board):
        self.board = board

        legal_moves = list(self.board.legal_moves)
        self.bestMove = random.choice(legal_moves)

        self.search(6, 0)

        return self.bestMove 

    def search(self, depth, ply, alpha=-INF, beta=INF):
        if self.board.is_win():
            return -INF
        if self.board.is_draw():
            return 0

        if depth <= 0:
            return self.evaluate()

        moves = list(self.board.legal_moves)
        random.shuffle(moves)
        bestScore = -INF-1

        for move in moves:
            self.board.push(move)
            score = -self.search(depth-1, ply+1, -beta, -alpha)
            self.board.pop()

            if score > bestScore:
                bestScore = score
                if ply == 0:
                    self.bestMove = move

            alpha = max(alpha, score)
            if alpha >= beta:
                break  # Alpha-beta pruning

        return bestScore

    def evaluate(self):
        score = 0
        
        # Check for vertical wins
        for col in range(7):
            for row in range(6 - 3):
                window = [self.board.grid[row + i][col] for i in range(4)]
                score += self.evaluate_window(window)

        # Check for horizontal wins
        for row in range(6):
            for col in range(7 - 3):
                window = [self.board.grid[row][col + i] for i in range(4)]
                score += self.evaluate_window(window)

        # Check for diagonal wins (top-left to bottom-right)
        for row in range(6 - 3):
            for col in range(7 - 3):
                window = [self.board.grid[row + i][col + i] for i in range(4)]
                score += self.evaluate_window(window)

        # Check for diagonal wins (bottom-left to top-right)
        for row in range(3, 6):
            for col in range(7 - 3):
                window = [self.board.grid[row - i][col + i] for i in range(4)]
                score += self.evaluate_window(window)

        return score

    def evaluate_window(self, window):
        player_piece = PLAYER_PIECE
        opponent_piece = OPPONENT_PIECE

        score = 0
        if window.count(player_piece) == 4:
            score += 100
        elif window.count(player_piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(player_piece) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opponent_piece) == 3 and window.count(0) == 1:
            score -= 4

        return score