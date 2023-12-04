from fourinarow import fourInRow
import importlib.util
import time
import concurrent.futures

def game():
    # Get bots
    spec1 = importlib.util.spec_from_file_location("bot1", "bot1/search.py")
    bot1_module = importlib.util.module_from_spec(spec1)
    spec1.loader.exec_module(bot1_module)
    bot1 = bot1_module.Bot()

    spec2 = importlib.util.spec_from_file_location("bot2", "bot2/search.py")
    bot2_module = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(bot2_module)
    bot2 = bot2_module.Bot()

    board = fourInRow.Board()
    # print(board.is_game_over())

    # Initialize time counters for each bot
    time_bot1 = 10
    time_bot2 = 10

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
                print("Time limit exceeded")
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
        board.push(move)
        print(board)

    # Print the result of the game
    if board.is_win():
        if board.turn:
            print("Bot 0 wins")
        else:
            print("Bot 1 wins")
    elif board.is_draw():
        print("The game is a draw")

if __name__ == "__main__":
    game()
