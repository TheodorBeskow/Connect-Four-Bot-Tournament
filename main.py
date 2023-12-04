from fourinarow import fourInRow
import importlib.util
import time


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
    print(board.is_game_over())

    # Play the game
    while not board.is_game_over():
        if board.turn:
            move = bot1.choose_move(board)
        else:
            move = bot2.choose_move(board)

        # Check if the move is legal
        if move not in list(board.legal_moves):
            print("Illegal move: " + str(move))
            break
        time.sleep(1)

        print(board)
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
