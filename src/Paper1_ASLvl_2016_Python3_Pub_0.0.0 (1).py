# Skeleton Program for the AQA AS1 Summer 2016 examination
# this code should be used in conjunction with the Preliminary Material
# written by the AQA AS1 Programmer Team
# developed in a Python 3 programming environment

# Version Number 1.0

import random


def get_row_column():
    valid = False
    while not valid:
        print()
        column = int(input("Please enter column: "))
        row = int(input("Please enter row: "))
        if column > 9 or column < 0 or row > 9 or row < 0:
            print("Sorry, that is outside the target area. Please select again.")
        else:
            valid = True
    print()
    return row, column


def make_player_move(board, ships):
    row, column = get_row_column()
    if board[row][column] == "m" or board[row][column] == "h":
        print("Sorry, you have already shot at the square (" + str(column) + "," + str(row) + "). Please try again.")
    elif board[row][column] == "-":
        print("Sorry, (" + str(column) + "," + str(row) + ") is a miss.")
        board[row][column] = "m"
        if radar_scan(board, row, column):
            print("Enemy near!")
        else:
            print("All quiet nearby.")
    else:
        ship_hit = ""
        pieces_left = ""
        for Ship in ships:
            if board[row][column] == Ship[0][0]:
                Ship[1] -= 1
                ship_hit = Ship[0]
                pieces_left = Ship[1]
        print("Hit " + ship_hit + " at (" + str(column) + "," + str(row) + ").")
        print("There are " + str(pieces_left) + " pieces of " + ship_hit + " left")
        if pieces_left == 0:
            print("YOU SANK THE " + ship_hit.upper())
        board[row][column] = "h"


def radar_scan(board, row, column):
    left_slice, right_slice, top_slice, bottom_slice = row-1, row+1, column-1, column+1
    if row == 0:
        left_slice = row
    elif row == 9:
        right_slice = row
    if column == 0:
        top_slice = column
    elif column == 9:
        bottom_slice = column
    for row_scan in range(left_slice, right_slice):
        for column_scan in range(top_slice, bottom_slice):
            if board[row][column] != "-" or board[row][column] != "m":
                return True
    return False


def set_up_board():
    board = []
    for Row in range(10):
        board_row = []
        for Column in range(10):
            board_row.append("-")
        board.append(board_row)
    return board


def set_up_scores():
    scores = [["George", 17],
             ["Paul", 19],
             ["John", 23],
             ["Ringo", 25],
             ["Bryan", 35]]
    return scores


def load_game(filename, board):
    board_file = open(filename, "r")
    for Row in range(10):
        line = board_file.readline()
        for Column in range(10):
            board[Row][Column] = line[Column]
    board_file.close()


def save_game(filename, board):
    board_file = open(filename, "w")
    board_save = ""
    for Row in range(10):
        for Column in range(10):
            board_save += board[Row][Column]
        board_save += "\n"
    board_file.write(board_save)
    board_file.close()


def place_random_ships(board, ships):
    for Ship in ships:
        valid = False
        while not valid:
            row = random.randint(0, 9)
            column = random.randint(0, 9)
            hvd = random.randint(0, 2)
            if hvd == 0:
                orientation = "v"
            elif hvd == 1:
                orientation = "h"
            else:
                orientation = "d"
            valid = validate_boat_position(board, Ship, row, column, orientation)
        print("Computer placing the " + Ship[0])
        place_ship(board, Ship, row, column, orientation)


def place_ships_manually(board, ships):
    for Ship in ships:
        valid = False
        while not valid:
            row = int(input("Please enter starting row for " + Ship[0] + ": "))
            column = int(input("Please enter starting column for " + Ship[0] + ": "))
            hvd = input("Please enter orientation of " + Ship[0] + " (horizontal/vertical/diagonal): ")
            orientation = hvd[0].lower()
            valid = validate_boat_position(board, Ship, row, column, orientation)
            if not valid:
                print("The co-ordinates entered were not valid. Please try again.\n")
        print("You have successfully placed the " + Ship[0])
        place_ship(board, Ship, row, column, orientation)
        real_board(board)


def place_ship(board, ship, row, column, orientation):
    if orientation == "v":
        for Scan in range(ship[1]):
            board[row + Scan][column] = ship[0][0]
    elif orientation == "h":
        for Scan in range(ship[1]):
            board[row][column + Scan] = ship[0][0]
    elif orientation == "d":
        for Scan in range(ship[1]):
            board[row + Scan][column + Scan] = ship[0][0]


def validate_boat_position(board, ship, row, column, orientation):
    if orientation == "v" and row + ship[1] > 10:
        return False
    elif orientation == "h" and column + ship[1] > 10:
        return False
    elif orientation == "d" and (column + ship[1] > 10 or row + ship[1] > 10):
        return False
    else:
        if orientation == "v":
            for Scan in range(ship[1]):
                if board[row + Scan][column] != "-":
                    return False
        elif orientation == "h":
            for Scan in range(ship[1]):
                if board[row][column + Scan] != "-":
                    return False
        elif orientation == "d":
            for Scan in range(ship[1]):
                if board[row + Scan][column + Scan] != "-":
                    return False
    return True


def check_win(board):
    for Row in range(10):
        for Column in range(10):
            if board[Row][Column] in ["A", "B", "S", "D", "P", "F"]:
                return False
    return True


def print_board(board):
    print()
    print("The board looks like this: ")
    print()
    print(" ", end="")
    for Column in range(10):
        print(" " + str(Column) + "  ", end="")
    print()
    for Row in range(10):
        print(str(Row) + " ", end="")
        for Column in range(10):
            if board[Row][Column] == "-":
                print(" ", end="")
            elif board[Row][Column] in ["A", "B", "S", "D", "P", "F"]:
                print(" ", end="")
            else:
                print(board[Row][Column], end="")
            if Column != 9:
                print(" | ", end="")
        print()


def real_board(board):
    print()
    print("The board looks like this: ")
    print()
    print(" ", end="")
    for Column in range(10):
        print(" " + str(Column) + "  ", end="")
    print()
    for Row in range(10):
        print(str(Row) + " ", end="")
        for Column in range(10):
            if board[Row][Column] == "-":
                print(" ", end="")
            else:
                print(board[Row][Column], end="")
            if Column != 9:
                print(" | ", end="")
        print()


def display_menu():
    print("MAIN MENU")
    print()
    print("1. Start new game")
    print("2. Load training game")
    print("3. Load saved game")
    print("4. Board Test")
    print("5. Manually place ships")
    print("6. Display high-score table")
    print("9. Quit")
    print()


def get_main_menu_choice():
    choice = int(input("Please enter your choice: "))
    print()
    return choice


def play_game(board, ships):
    game_won = False
    torpedoes = 20
    while not game_won and torpedoes != 0:
        print_board(board)
        make_player_move(board, ships)
        torpedoes -= 1
        print("Torpedoes left: " + str(torpedoes))
        check_save = input("Would you like to save the game (Y/N): ").lower()
        if check_save == "y":
            file_name = input("Enter file name to save as: ")
            save_game(file_name, Board)
        game_won = check_win(board)
        if game_won:
            print("All ships sunk!")
            print()
        if torpedoes == 0:
            print("GAME OVER! You ran out of ammo.")
            print()


def display_high_scores(scores):
    player_name = input("Type your name: ")
    if player_name != "":
        player_score = int(input("Type your score: "))
        if player_score <= scores[4][1]:
            scores[4][0] = player_name
            scores[4][1] = player_score
    bub_sort_scores(scores)
    # Make a nice table
    col1_width = 12
    col2_width = 4
    hr = "-" * (col1_width + col2_width + 3)
    print(hr)
    for score_entry in scores:
        col1_gap_end = " " * (col1_width - (len(score_entry[0]) + 1))
        if score_entry[1] >= 10:
            width_col2_content = 2
        else:
            width_col2_content = 1
        col2_gap_end = " " * (col2_width - (width_col2_content + 1))
        print("| " + score_entry[0] + col1_gap_end + "| " + str(score_entry[1]) + col2_gap_end + "|\n" + hr)


def bub_sort_scores(scores):
    changes_made = True
    while changes_made:
        changes_made = False
        for i in range(len(scores) - 1):
            if scores[i][1] > scores[i+1][1]:
                scores[i], scores[i+1] = scores[i+1], scores[i]
                changes_made = True


if __name__ == "__main__":
    training_game = "Training.txt"
    MenuOption = 0
    score = set_up_scores()
    while not MenuOption == 9:
        Board = set_up_board()
        Ships = [["Aircraft Carrier", 5],
                 ["Battleship", 4],
                 ["Submarine", 3],
                 ["Destroyer", 3],
                 ["Patrol Boat", 2],
                 ["Frigate", 3]]
        display_menu()
        MenuOption = get_main_menu_choice()
        if MenuOption == 9:
            check_end = input("Are you sure? (y/n): ").lower()
            if check_end == "n":
                MenuOption = 0
        if MenuOption == 1:
            place_random_ships(Board, Ships)
            play_game(Board, Ships)
        if MenuOption == 2:
            load_game(training_game, Board)
            play_game(Board, Ships)
        if MenuOption == 3:
            game_to_load = input("Enter filename to open: ")
            load_game(game_to_load, Board)
            play_game(Board, Ships)
        if MenuOption == 4:
            place_random_ships(Board, Ships)
            real_board(Board)
        if MenuOption == 5:
            place_ships_manually(Board, Ships)
            play_game(Board, Ships)
        if MenuOption == 6:
            print("High score table:\n")
            display_high_scores(score)
