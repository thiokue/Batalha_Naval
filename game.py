import random
import string
import os


def criar_tabuleiro():
    """
    Create a game board with dimensions 15x15.

    Returns:
    tabuleiro (list): A 2D list representing the game board.
    """
    tabuleiro = []
    for i in range(0,15):
        lista = []
        for x in range(0,15):
            lista.append(0)
        tabuleiro.append(lista)
    return tabuleiro


def generate_coords():
    """
    Generate random coordinates for placing a game piece.

    Returns:
    coords (str): A string representing the coordinates and orientation of the game piece.
    """
    y_axis = random.choice(string.ascii_uppercase[:14])
    x_axis = random.randint(1, 14)
    orientation = random.choice(['H', 'V'])
    return y_axis + str(x_axis) + orientation


def colocar_pecas(tabuleiro, pecas, peca_id, max_attempts=1000):
    """
    Place a game piece on the game board.

    Args:
    tabuleiro (list): The game board.
    pecas (dict): A dictionary containing the game pieces.
    peca_id (str): The ID of the game piece to be placed.
    max_attempts (int): The maximum number of attempts to place a piece.

    Returns:
    coords_list (list): A list of coordinates and orientations of the placed game pieces.
    """
    coords_list = []
    for peca in pecas[peca_id]:
        for _ in range(max_attempts):
            coords = generate_coords()
            x = ord(coords[0]) - ord('A')
            y = int(coords[1:-1]) - 1
            axis = coords[-1]
            if axis == 'H':
                if y + len(peca) > len(tabuleiro[0]) or any(tabuleiro[x][y+i] != 0 for i in range(len(peca))):
                    continue
                for i in range(len(peca)):
                    tabuleiro[x][y+i] = peca[i]
            else:
                if x + len(peca) > len(tabuleiro) or any(tabuleiro[x+i][y] != 0 for i in range(len(peca))):
                    continue
                for i in range(len(peca)):
                    tabuleiro[x+i][y] = peca[i]
            coords_list.append(coords)
            break
        else:
            raise Exception(f"ERROR_OVERWRITE_PIECES_VALIDATION: PIECE {peca_id} | ATTEMPTS {max_attempts}")
    return coords_list


def create_player_file(filename, piece_coords):
    """
    Write the player's pieces to a text file.

    Args:
    filename (str): The name of the file to write to.
    piece_coords (dict): A dictionary containing the coordinates of the player's pieces.

    Returns:
    None
    """
    with open(filename, 'w') as f:
        for key in piece_coords:
            coords_str = ' | '.join(piece_coords[key])
            f.write(f"{key}:{coords_str}\n")


def write_game_state(piece_coords1, piece_coords2):
    """
    Write the game state to a text file.

    Args:
    piece_coords1 (dict): A dictionary containing the coordinates of Player 1's pieces.
    piece_coords2 (dict): A dictionary containing the coordinates of Player 2's pieces.

    Returns:
    None
    """
    with open('game_state.txt', 'w') as f:
        f.write("Player 1 pieces:\n")
        for key in piece_coords1:
            coords_str = ' | '.join(piece_coords1[key])
            f.write(f"{key}:{coords_str}\n")
        f.write("\nPlayer 2 pieces:\n")
        for key in piece_coords2:
            coords_str = ' | '.join(piece_coords2[key])
            f.write(f"{key}:{coords_str}\n")
        f.write(f"Plays:\nT;")


def attempt_hit(guess, tabuleiro):
    """
    Attempt to hit a game piece on the game board.

    Args:
    guess (str): The guess made by the player.
    tabuleiro (list): The game board.

    Returns:
    hit (bool): True if the guess hits a game piece, False otherwise.
    already_hit (bool): True if the spot was already hit, False otherwise.
    """
    if not guess or not (guess[0].isalpha() and guess[1:].isdigit()):
        raise ValueError("ERROR_POSITION_NONEXISTENT_VALIDATION")
    x = ord(guess[0].lower()) - ord('a')
    y = int(guess[1:]) - 1
    if tabuleiro[x][y] != 0:
        already_hit = tabuleiro[x][y] == 'X'
        tabuleiro[x][y] = 'X'  # Mark the piece as hit
        return True, already_hit
    else:
        return False, False


def is_valid_guess(guess, max_x, max_y):
    """
    Check if a guess is valid.

    Args:
    guess (str): The guess made by the player.
    max_x (int): The maximum value for the x-axis.
    max_y (int): The maximum value for the y-axis.

    Returns:
    valid (bool): True if the guess is valid, False otherwise.
    """
    return guess and guess[0].isalpha() and guess[1:].isdigit() and 0 < int(guess[1:]) <= max_y and ord(guess[0].lower()) - ord('a') + 1 <= max_x


def count_pieces(tabuleiro):
    """
    Count the number of game pieces on the game board.

    Args:
    tabuleiro (list): The game board.

    Returns:
    count (int): The number of game pieces.
    """
    return sum(cell != 0 for row in tabuleiro for cell in row)

def print_boards(board1, board2):
    """
    Print two game boards side by side.

    Args:
    board1 (list): The first game board.
    board2 (list): The second game board.

    Returns:
    None
    """
    # Calculate the width of the boards
    width1 = len(' '.join(map(str, board1[0])))
    width2 = len(' '.join(map(str, board2[0])))

    # Print the titles
    print(f"{'Board 1':<{width1}}\t\t{'Board 2':<{width2}}")

    # Print the boards
    for row1, row2 in zip(board1, board2):
        print(' '.join(map(str, row1)), '\t\t', ' '.join(map(str, row2)))

#MAIN

pecas = {
    '1': [[1,1,1,1] for _ in range(5)],
    '2': [[1,1,1,1,1] for _ in range(2)],
    '3': [[1] for _ in range(10)],
    '4': [[1,1] for _ in range(5)]
}

# Delete existing .txt files
if os.path.exists("player1.txt"):
    os.remove("player1.txt")
if os.path.exists("player2.txt"):
    os.remove("player2.txt")
if os.path.exists("output.txt"):
    os.remove("output.txt")

# Creating the matrices
tabuleiro1 = criar_tabuleiro()
tabuleiro2 = criar_tabuleiro()

# Putting the pieces
piece_coords1 = {}
piece_coords2 = {}
for key in pecas:
    piece_coords1[key] = colocar_pecas(tabuleiro1, pecas, key)
    piece_coords2[key] = colocar_pecas(tabuleiro2, pecas, key)

# Create an .txt with coordinates of the pieces for each player
create_player_file('player_1.txt', piece_coords1)
create_player_file('player_2.txt', piece_coords2)

# create the output.txt file with data from both players
write_game_state(piece_coords1, piece_coords2)

# GameStart
total_pieces1 = sum(len(piece) for pieces in pecas.values() for piece in pieces)
total_pieces2 = total_pieces1
hits1 = 0
hits2 = 0
max_x = len(tabuleiro1)
max_y = len(tabuleiro1[0])


# Initialize attempt counters
attempts1 = 0
attempts2 = 0

# Initialize score counters
score1 = 0
score2 = 0

# main game loop
while True:
    for i in range(2):  # Loop for two players
        # Check if player has remaining attempts
        if (i == 0 and attempts1 >= 25) or (i == 1 and attempts2 >= 25):
            continue

        while True:
            guess = input(str(f"Player {i+1}, Guess: "))
            if is_valid_guess(guess, max_x, max_y):
                break
            else:
                print("ERROR_POSITION_NONEXISTENT_VALIDATION")
        if i == 0:
            print(f'Remaining Attempts for Player {i+1}: {25 - attempts1}')
            hit, already_hit = attempt_hit(guess, tabuleiro2)
            play = f'J{i+1}{guess}'
            if hit:
                if not already_hit:
                    score1 += 3
                    hits1 += 1
                    print("Hit!")
                    if hits1 == total_pieces2:
                        score1 += 5  # Extra points for hitting all pieces in a piece
                        print(f"Player 1 has won.")
                        print_boards(tabuleiro1, tabuleiro2)
                        break
                else:
                    print("You've already hit this spot!")
            else:
                print("Miss!")
            attempts1 += 1
        else:
            print(f'Remaining Attempts for Player {i+1}: {25 - attempts2}')
            hit, already_hit = attempt_hit(guess, tabuleiro1)
            play = f'J{i+1}{guess}'
            if hit:
                if not already_hit:
                    score2 += 3
                    hits2 += 1
                    print("Hit!")
                    if hits2 == total_pieces1:
                        score2 += 5  # Extra points for hitting all pieces in a piece
                        print(f"Player 2 has won.")
                        print_boards(tabuleiro1, tabuleiro2)
                else:
                    print("You've already hit this spot!")
            else:
                print("Miss!")
            attempts2 += 1
        with open('game_state.txt', 'a') as f:
            f.write(f'{play.upper()}|')        
    if (attempts1 >= 25 and attempts2 >= 25):
        print('No more attempts. Game over.')
        print(f'Player 1 score: {score1}')
        print(f'Player 2 score: {score2}')
        print_boards(tabuleiro1, tabuleiro2)
        break

# Determine the winner and their stats
if score1 > score2:
    winner_info = f'J1 {hits1}AA {25 - hits1}AE {score1}PT'
elif score2 > score1:
    winner_info = f'J2 {hits2}AA {25 - hits2}AE {score2}PT'
else:  # It's a draw
    winner_info = f'J1 {hits1}AA {25 - hits1}AE {score1}PT\nJ2 {hits2}AA {25 - hits2}AE {score2}PT'

# Record the game end information
with open('game_state.txt', 'a') as f:
    f.write(f'\n{winner_info}')