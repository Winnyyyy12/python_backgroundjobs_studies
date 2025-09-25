import asyncio
import random


def print_board(board):
    print("\n")
    for i in range(0, 9, 3):
        print(" | ".join(board[i:i+3]))
        if i < 6:
            print("-" * 9)
    print("\n")

# Check Winner


def check_winner(board, symbol):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],   # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],   # Columns
        [0, 4, 8], [2, 4, 6]               # Diagonals
    ]
    return any(all(board[i] == symbol for i in cond) for cond in win_conditions)

# Async Player Task


async def player(name, symbol, moves_queue):
    while True:
        await asyncio.sleep(random.uniform(0.5, 2))  # Random delay
        move = random.randint(0, 8)                  # Random move
        await moves_queue.put((name, symbol, move))  # Send move to game engine

# Game Engine Task


async def game_engine(moves_queue):
    board = [" "] * 9
    players = ["X", "O"]
    turn = 0
    moves_made = 0

    print("Game Started: Tic Tac Toe\n")
    print_board(board)

    while moves_made < 9:
        name, symbol, move = await moves_queue.get()  # Wait for a player's move

        # Check if it's this player's turn
        if symbol != players[turn]:
            continue                                  # Ignore if wrong turn

        # If spot is already taken
        if board[move] != " ":
            print(f"{name} tried to play at {move}, but it's taken!")
            continue

        # Place the move
        board[move] = symbol
        print(f"{name} ({symbol}) played at {move}")
        print_board(board)

        moves_made += 1

        # Check for winner
        if check_winner(board, symbol):
            print(f"{name} ({symbol}) WINS!")
            return

        # Switch turn
        turn = 1 - turn

    print("It's a draw!")

# Main Async Entry Point


async def main():
    moves_queue = asyncio.Queue()

    # Two players
    p1 = asyncio.create_task(player("Winny", "X", moves_queue))
    p2 = asyncio.create_task(player("Junie", "O", moves_queue))

    # Game engine
    await game_engine(moves_queue)

    # Cancel players after game ends
    p1.cancel()
    p2.cancel()

# Run the game
asyncio.run(main())
