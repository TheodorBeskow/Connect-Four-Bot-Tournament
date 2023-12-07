from connect4 import Connect4
import random


class Bot:
    def choose_move(self, board):
        self.board = board

        legal_moves = list(self.board.legal_moves)
        bestmove = random.choice(legal_moves)

        return bestmove 