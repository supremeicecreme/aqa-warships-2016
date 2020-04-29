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
    else:
        print("Hit at (" + str(column) + "," + str(row) + ").")
        board[row][column] = "h"


def set_up_board():
    board = []
    for Row in range(10):
        board_row = []
        for Column in range(10):
            board_row.append("-")
        board.append(board_row)
    return board


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
            h_or_v = random.randint(0, 1)
            if h_or_v == 0:
                orientation = "v"
            else:
                orientation = "h"
            valid = validate_boat_position(board, Ship, row, column, orientation)
        print("Computer placing the " + Ship[0])
        place_ship(board, Ship, row, column, orientation)


def place_ship(board, ship, row, column, orientation):
    if orientation == "v":
        for Scan in range(ship[1]):
            board[row + Scan][column] = ship[0][0]
    elif orientation == "h":
        for Scan in range(ship[1]):
            board[row][column + Scan] = ship[0][0]


def validate_boat_position(board, ship, row, column, orientation):
    if orientation == "v" and row + ship[1] > 10:
        return False
    elif orientation == "h" and column + ship[1] > 10:
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
    return True


def check_win(board):
    for Row in range(10):
        for Column in range(10):
            if board[Row][Column] in ["A", "B", "S", "D", "P"]:
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
            elif board[Row][Column] in ["A", "B", "S", "D", "P"]:
                print(" ", end="")
            else:
                print(board[Row][Column], end="")
            if Column != 9:
                print(" | ", end="")
        print()


def print_test_board(board):
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
    print("9. Quit")
    print()


def get_main_menu_choice():
    print("Please enter your choice: ", end="")
    choice = int(input())
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


if __name__ == "__main__":
    training_game = "Training.txt"
    MenuOption = 0
    while not MenuOption == 9:
        Board = set_up_board()
        Ships = [["Aircraft Carrier", 5], ["Battleship", 4], ["Submarine", 3], ["Destroyer", 3], ["Patrol Boat", 2]]
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
            print_test_board(Board)
