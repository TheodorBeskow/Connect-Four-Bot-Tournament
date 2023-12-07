class Connect4:
    class Board:
        def __init__(self):
            self.rows = 6
            self.cols = 7
            self.grid = [[-1 for i in range(self.cols)] for i in range(self.rows)]
            self.turn = 1
            self.move_stack = []
            self.legal_moves = self.generate_legal_moves()
        
        def __str__(self):
            s = []
            for row in range(self.rows - 1, -1, -1):
                for col in range(self.cols):
                    if self.grid[row][col] != -1:
                        s.append(' ')
                    s.append(str(self.grid[row][col]))
                    s.append(' ')
                s[-1] = '\n'
            return "".join(s)

        def is_game_over(self): # four in a row or filled
            if self.is_win() or self.is_draw():
                return True
            return False
        
        def generate_legal_moves(self): # all legal moves, list with col indexes
            moves = []
            for col in range(self.cols):
                if self.grid[-1][col] == -1:
                    moves.append(col)
            return moves # maybe return [] if self.is_game_over()
        
        def is_win(self): # has four in row
            # check rows
            win = False
            for row in range(self.rows):
                for col in range(self.cols - 3): # in this row, check all starting columns
                    li = []
                    for c in range(col, col + 4):
                        li.append(self.grid[row][c])
                    
                    if li.count(0) == 4 or li.count(1) == 4:
                        win = True
            
            # check columns
            for col in range(self.cols):
                for row in range(self.rows - 3): # in this row, check all starting columns
                    li = []
                    for r in range(row, row + 4):
                        li.append(self.grid[r][col])
                    
                    if li.count(0) == 4 or li.count(1) == 4:
                        win = True

            # check diagonals
            for row in range(self.rows):
                for col in range(self.cols - 3):
                    li1 = []
                    li2 = []
                    for k in range(4):
                        if row + k < self.rows:
                            li1.append(self.grid[row + k][col + k])
                        if row - k >= 0:
                            li2.append(self.grid[row - k][col + k])
                    
                    if li1.count(0) == 4 or li1.count(1) == 4:
                        win = True

                    if li2.count(0) == 4 or li2.count(1) == 4:
                        win = True

            return win

        def is_draw(self): # is filled
            if len(self.legal_moves) == 0 and self.is_win() == False:
                return True
            return False
        
        def push(self, col: int): # put in column "col"
            if col not in self.legal_moves:
                print("INVALID MOVE")
                assert 0
            
            row = 0
            for r in range(self.rows):
                if self.grid[r][col] == -1:
                    row = r
                    break
            
            self.grid[row][col] = self.turn
            self.move_stack.append(col)
            self.turn ^= 1
            self.legal_moves = self.generate_legal_moves()
    
        def pop(self): # undo last move
            col = self.move_stack.pop()
            row = 0

            for r in range(self.rows - 1, -1, -1):
                if self.grid[r][col] == -1:
                    row = r
                    break
            
            self.grid[row][col] = -1
            self.turn ^= 1
            self.legal_moves = self.generate_legal_moves()

        def pop(self): # undo last move
            col = self.move_stack.pop()
            row = 0

            for r in range(self.rows - 1, -1, -1):
                if self.grid[r][col] != -1:
                    row = r
                    break
            
            self.grid[row][col] = -1
            self.turn ^= 1
            self.legal_moves = self.generate_legal_moves()

    def __init__(self):
        pass

board = Connect4.Board()