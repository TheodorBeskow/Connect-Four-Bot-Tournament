from connect4 import Connect4
import random

INF = 1000000

class Bot:
    def __init__(self):
        self.board = None
        self.bestMove = None
        self.startTime = None
    
    def choose_move(self, board):
        self.board = board
        self.bestMove = None
        self.search(4, 0)
        return self.bestMove 

    def search(self, depth, ply):
        if self.board.is_win():
            return -INF
        if self.board.is_draw() or depth == 0:
            return self.evaluate()

        moves = list(self.board.legal_moves)
        random.shuffle(moves)
        bestScore = -INF-1

        for move in moves:
            self.board.push(move)
            score = -self.search(depth-1, ply+1)
            self.board.pop()

            if score > bestScore:
                bestScore = score
                if ply == 0:
                    self.bestMove = move

        return bestScore
        
    def evaluate(self):
            score = 0

            # Evaluate based on connected pieces
            score += self.evaluate_connected(1)  # Player 1's pieces
            score -= self.evaluate_connected(-1)  # Player 2's pieces

            return score

    def evaluate_connected(self, player):
            # Evaluate the board based on connected pieces for the given player
            connected_score = 0

            for row in range(self.board.rows):
                for col in range(self.board.cols):
                    if self.board.grid[row][col] == player:
                        # Horizontal
                        connected_score += self.count_connected(row, col, player, 0, 1)

                        # Vertical
                        connected_score += self.count_connected(row, col, player, 1, 0)

                        # Diagonal (top-left to bottom-right)
                        connected_score += self.count_connected(row, col, player, 1, 1)

                        # Diagonal (bottom-left to top-right)
                        connected_score += self.count_connected(row, col, player, -1, 1)

            return connected_score

    def count_connected(self, row, col, player, row_delta, col_delta):
            count = 0

            for i in range(4):
                r = row + i * row_delta
                c = col + i * col_delta

                if 0 <= r < self.board.rows and 0 <= c < self.board.cols:
                    if self.board.grid[r][c] == player:
                        count += 1
                    else:
                        break
                else:
                    break

            return count