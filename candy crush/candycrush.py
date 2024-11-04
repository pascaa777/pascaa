import random

GRID_DIMENSION = 11
EMPTY_CELL = 0
CANDY_TYPES = [1, 2, 3, 4] 

SCORE_3_IN_ROW = 5
SCORE_4_IN_ROW = 10
SCORE_5_IN_ROW = 50
SCORE_L_SHAPE = 20
SCORE_T_SHAPE = 30
GOAL_SCORE = 10000

total_score = 0
move_counter = 0

NUMBER_OF_GAMES = 100

def create_board():
    return [[random.choice(CANDY_TYPES) for _ in range(GRID_DIMENSION)] for _ in range(GRID_DIMENSION)]

def display_board(board):
    for row in board:
        print(" ".join(str(cell) if cell != EMPTY_CELL else " " for cell in row))
    print()

def locate_matches(board):
    matches_to_clear = set()
    global total_score

    for length, points in [(5, SCORE_5_IN_ROW), (4, SCORE_4_IN_ROW), (3, SCORE_3_IN_ROW)]:
        matches_to_clear.update(check_straight_matches(board, length, points))
    
    matches_to_clear.update(find_t_shapes(board))
    matches_to_clear.update(find_l_shapes(board))

    return matches_to_clear

def check_straight_matches(board, length, points):
    found_matches = set()
    global total_score

    for row in range(GRID_DIMENSION):
        for col in range(GRID_DIMENSION - length + 1):
            if board[row][col] != EMPTY_CELL and all(board[row][col] == board[row][col + offset] for offset in range(length)):
                found_matches.update((row, col + offset) for offset in range(length))
                total_score += points

    for col in range(GRID_DIMENSION):
        for row in range(GRID_DIMENSION - length + 1):
            if board[row][col] != EMPTY_CELL and all(board[row][col] == board[row + offset][col] for offset in range(length)):
                found_matches.update((row + offset, col) for offset in range(length))
                total_score += points

    return found_matches

def find_t_shapes(board):
    found_matches = set()
    global total_score

    for row in range(GRID_DIMENSION - 2):
        for col in range(1, GRID_DIMENSION - 1):
            if board[row][col] != EMPTY_CELL and all(
                board[row][col] == board[row + dx][col + dy]
                for dx, dy in [(0, 0), (1, -1), (1, 0), (1, 1), (2, 0)]
            ):
                found_matches.update((row + dx, col + dy) for dx, dy in [(0, 0), (1, -1), (1, 0), (1, 1), (2, 0)])
                total_score += SCORE_T_SHAPE

    return found_matches

def find_l_shapes(board):
    found_matches = set()
    global total_score

    for row in range(GRID_DIMENSION - 2):
        for col in range(GRID_DIMENSION - 2):
            if board[row][col] != EMPTY_CELL and all(
                board[row][col] == board[row + dx][col + dy]
                for dx, dy in [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
            ):
                found_matches.update((row + dx, col + dy) for dx, dy in [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)])
                total_score += SCORE_L_SHAPE

    return found_matches

def clear_matches(board, matches):
    for (row, col) in matches:
        board[row][col] = EMPTY_CELL

def collapse_and_refill(board):
    for col in range(GRID_DIMENSION):
        column_stack = [board[row][col] for row in range(GRID_DIMENSION) if board[row][col] != EMPTY_CELL]

        new_candies = [random.choice(CANDY_TYPES) for _ in range(GRID_DIMENSION - len(column_stack))]
        updated_column = new_candies + column_stack
        
        for row in range(GRID_DIMENSION):
            board[row][col] = updated_column[row]

def suggest_move(board):
    for row in range(GRID_DIMENSION):
        for col in range(GRID_DIMENSION):
            if col < GRID_DIMENSION - 1: 
                board[row][col], board[row][col + 1] = board[row][col + 1], board[row][col]
                if locate_matches(board):
                    board[row][col], board[row][col + 1] = board[row][col + 1], board[row][col]
                    return (row, col), (row, col + 1)
                board[row][col], board[row][col + 1] = board[row][col + 1], board[row][col]
            if row < GRID_DIMENSION - 1: 
                board[row][col], board[row + 1][col] = board[row + 1][col], board[row][col]
                if locate_matches(board):
                    board[row][col], board[row + 1][col] = board[row + 1][col], board[row][col]
                    return (row, col), (row + 1, col)
                board[row][col], board[row + 1][col] = board[row + 1][col], board[row][col]
    return None  

def play():
    global total_score, move_counter
    board = create_board()
    game_ongoing = True

    while game_ongoing and total_score < GOAL_SCORE:
        print(f"Current Board (Score: {total_score})")
        display_board(board)

        matches = locate_matches(board)
        if matches:
            clear_matches(board, matches)
            collapse_and_refill(board)
        else:
            move = suggest_move(board)
            if move:
                (x1, y1), (x2, y2) = move
                print(f"Suggested Move: Swap ({x1}, {y1}) with ({x2}, {y2})")
                board[x1][y1], board[x2][y2] = board[x2][y2], board[x1][y1]
                move_counter += 1
            else:
                game_ongoing = False 
    print("Final Board:")
    display_board(board)
    return total_score, move_counter

def run_multiple_games(num_games):
    total_moves = 0
    for game_number in range(1, num_games + 1):
        global total_score, move_counter
        total_score, move_counter = 0, 0
        print(f"--- Game {game_number} ---")
        final_score, moves = play()
        print(f"Final Score for Game {game_number}: {final_score}")
        print(f"Total Moves for Game {game_number}: {moves}\n")
        total_moves += moves

    average_moves = total_moves / num_games if num_games > 0 else 0
    print(f"Average number of moves over {num_games} games: {average_moves:.2f}")

run_multiple_games(NUMBER_OF_GAMES)