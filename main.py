from connect4 import Connect4
import importlib.util
import time
import concurrent.futures
import pygame

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
     
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):      
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 0: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()
    

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
 
ROW_COUNT = 6
COLUMN_COUNT = 7

#initalize pygame
pygame.init()
 
#define our screen size
SQUARESIZE = 100
 
#define width and height of board
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
 
size = (width, height)
 
RADIUS = int(SQUARESIZE/2 - 5)
 
screen = pygame.display.set_mode(size)
myfont = pygame.font.SysFont("monospace", 65)

def game():
    # Get bots
    name1 = "EnemyBot"
    spec1 = importlib.util.spec_from_file_location("bot1", f"Bots/{name1}/minimax.py")
    bot1_module = importlib.util.module_from_spec(spec1)
    spec1.loader.exec_module(bot1_module)
    bot1 = bot1_module.Bot()

    name2 = "YourBot"
    spec2 = importlib.util.spec_from_file_location("bot2", f"Bots/{name2}/minimax.py")
    bot2_module = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(bot2_module)
    bot2 = bot2_module.Bot()

    board = Connect4.Board()

    # Initialize time counters for each bot
    time_bot1 = 10
    time_bot2 = 10

    draw_board(board.grid)
    # Play the game
    while not board.is_game_over():
        start_time = time.time()
        if board.turn:
            bot = bot1
            remaining_time = time_bot1
        else:
            bot = bot2
            remaining_time = time_bot2

        # Run the bot's choose_move function with a timeout
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(bot.choose_move, board)
            try:
                move = future.result(timeout=remaining_time)
            except concurrent.futures.TimeoutError:
                print((name2 if board.turn else name1) + " won by time!!")
                break

        end_time = time.time()
        elapsed_time = end_time - start_time

        # Update time counters
        if board.turn:
            time_bot1 -= elapsed_time
        else:
            time_bot2 -= elapsed_time

        # Check if the move is legal
        if move not in list(board.legal_moves):
            print("Illegal move: " + str(move))
            break

        print(time_bot1, time_bot2)
        print("----------")
        time.sleep(0.3)
        board.push(move)
        
        # Display board in pygame window
        draw_board(board.grid)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  
                return

    # Print the result of the game
    if board.is_win():
        if board.turn:
            label = myfont.render(f"{name2} wins!!", 1, YELLOW)
            screen.blit(label, (40,10))
        else:
            label = myfont.render(f"{name1} wins!!", 1, RED)
            screen.blit(label, (40,10))
    elif board.is_draw():
        label = myfont.render(f"{name2} wins!!", 1, YELLOW)
        screen.blit(label, (40,10))
    
    draw_board(board.grid)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

if __name__ == "__main__":
    game()
