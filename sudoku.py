# 1. Name:
#      Nathan Bird
# 2. Assignment Name:
#      Lab 06 : Sudoku Program
# 3. Assignment Description:
#      Complete sudoku program.
# 4. What was the hardest part? Be as specific as possible.
#      This part of the assignment went extremely smoothly for me
#      because all I really had to do was implement the design I had already
#      conceived in my pseudocode to get the legal values for a particular
#      square.
# 5. How long did it take for you to complete the assignment?
#      Including some time I spent last week working on this updated and
#      quasi-refactored version of the draft program, I would say I spent
#      around 3-4 hours or so working on this week's assignment, most of which
#      time was spent on coming up with and trying to video the test cases.


import json

# from json_no_indent import NoIndent, NoIndentEncoder

LAST_USED_FILE = ".last-used.txt"

def read_board() -> list[list]:
    """Prompt user for location of board and convert json file to 2d list."""
    board = {}
    board_file = None
    file_chosen = False
    while not file_chosen:
        try:
            with open(LAST_USED_FILE, "r") as file:
                board_file = file.read()
        except FileNotFoundError:
            # print(f"DEBUG: `{LAST_USED_FILE}` could not be found. ")
            pass
        if board_file:
            use_saved = input(f"Continue where you left off? <{board_file}> (Y/N): ")
        if not board_file or use_saved.lower() != "y":
            board_file = input("Where is your board located?: ")
        try:
            with open(board_file, "r") as file:
                board = json.loads(file.read())
                file_chosen = True
        except FileNotFoundError:
            print(
                f"ERROR: `{board_file}` could not be found. "
                f"Please enter a valid path to a sudoku file."
            )
        except json.decoder.JSONDecodeError:
            print(
                f"ERROR: `{board_file}` could not be read. "
                f"Please enter a valid path to a sudoku `.json` file."
            )
        except Exception:
            print(f"ERROR: There was a problem with `{board_file}`.")
    return board["board"]


def display_board(board, cursor_row=None, cursor_col=None):
    """Displays the given 2d list `board`.

    If passed `cursor_row` AND `cursor_col`, that square prints as highlighted.
    """

    assert type(board) == type([[]])
    if cursor_row and cursor_col:
        assert type(cursor_col) == type(0)
        assert type(cursor_row) == type(0)
        assert 0 <= cursor_row <= 8
        assert 0 <= cursor_col <= 8

    seps = "  |  |  \n"
    print()
    print(f"   A B C D E F G H I")
    for i_row, row in enumerate(board):
        if i_row % 3 == 0 and i_row != 0:
            print(f"   -----+-----+-----")
        print(f"{i_row+1}  ", end="")
        for i_col in range(len(board[i_row])):
            # Optionally highlight the square the user picked to edit.
            if i_row == cursor_row and i_col == cursor_col:
                value = "█"
                # value = "▢"
            # Display 0s in the board object as blank spaces.
            else:
                value = board[i_row][i_col] if board[i_row][i_col] != 0 else " "
            print(f"{value}{seps[i_col]}", end="")
    print()


def is_coord_valid(coord: str) -> bool:
    """Returns true if the coordinate string is in a valid format."""
    # IF length is two characters
    #      AND
    #      ((first character is letter
    #       AND first character is between A-I
    #       AND second character is number
    #       AND second character is between 1-9)
    #      OR
    #      (second character is letter
    #       AND second character is between A-I
    #       AND first character is number
    #       AND first character is between 1-9))
    #   RETURN TRUE
    return len(coord) == 2 and (
        (
            coord[0].isalpha()
            and ord("A") <= ord(coord[0].upper()) <= ord("I")
            and coord[-1].isdigit()
            and ord("1") <= ord(coord[-1]) <= ord("9")
        )
        or (
            coord[-1].isalpha()
            and ord("A") <= ord(coord[-1].upper()) <= ord("I")
            and coord[0].isdigit()
            and ord("1") <= ord(coord[0]) <= ord("9")
        )
    )


def parse_input(coordinate: str) -> tuple:
    """Take the coordinate the user entered and convert to
    row/column (2d list) indicies.
    """
    assert len(coordinate) == 2
    assert coordinate.isupper()
    assert (coordinate[0].isalpha() and coordinate[-1].isdigit()) or (
        coordinate[-1].isalpha() and coordinate[0].isdigit()
    )

    # Split up the coordinate into letter (col) and number (row).
    if coordinate[0].isalpha() and coordinate[-1].isdigit():
        letter = coordinate[0]
        number = int(coordinate[-1])
    else:
        letter = coordinate[-1]
        number = int(coordinate[0])

    assert letter.isalpha()
    assert ord("A") <= ord(letter) <= ord("I")  # A-I
    assert 1 <= number <= 9

    col = ord(letter) - ord("A")
    row = number - 1
    return row, col


def get_illegal_moves(board, row, col) -> dict:
    """Gets all illegal moves for the indicated square (at board[row][col])."""
    illegal_moves = {}

    # Check row
    for value in board[row]:
        if value != 0:
            illegal_moves[value] = "ROW"

    # Check column
    for i in range(len(board)):
        value = board[i][col]
        if value != 0:
            if value not in illegal_moves.keys():
                illegal_moves[value] = "COL"
            else:
                illegal_moves[value] += ", COL"

    # Check 3x3 box
    box_row_reset = (row // 3) * 3
    box_col_reset = (col // 3) * 3
    for i in range(box_row_reset, box_row_reset + 3):
        for j in range(box_col_reset, box_col_reset + 3):
            value = board[i][j]
            if value != 0:
                if value not in illegal_moves.keys():
                    illegal_moves[value] = "BOX"
                else:
                    illegal_moves[value] += ", BOX"

    return illegal_moves


def write_board(board):
    """Get location to save board and write to file."""
    # board_json = {'board':[NoIndent(row) for row in board]}   # Using json_no_indent
    board_json = {"board": board}  # Not using json_no_indent
    file_written = False
    board_file = None
    while not file_written:
        try:
            with open(LAST_USED_FILE, "r") as file:
                board_file = file.read()
        except FileNotFoundError:
            # print(f"DEBUG: `{LAST_USED_FILE}` could not be found. ")
            pass
        if board_file:
            use_saved = input(f"Save where you left off? <{board_file}> (Y/N): ")
        if not board_file or use_saved.lower() != "y":
            board_file = input("Where do you want to save your board?: ")
        try:
            with open(board_file, "w") as file:
                # file.write(json.dumps(obj=board_json,
                #                       cls=NoIndentEncoder,      # Using json_no_indent
                #                       indent=2,
                #                       separators=(', ', ':')))
                file.write(json.dumps(board_json))  # Not using json_no_indent
                file_written = True
            if file_written:
                with open(LAST_USED_FILE, "w") as file:
                    file.write(board_file)
        except FileNotFoundError:
            print(f"ERROR: Must specify an output file. Cannot be NULL.")


def play_round(board) -> bool:
    """Play a round of the game.

    Get coordinate to edit from user, then get the value at that square.
    """
    action_taken = False
    while not action_taken:
        display_board(board)
        action = input("Specify a coordinate to edit or 'Q' to save and quit.\n> ")
        # Save and Quit.
        if action.lower() == "q":
            action_taken = True
            write_board(board)
            return True
        # If editing a valid square:
        elif is_coord_valid(action):
            coord = action.upper() if action[0].isalpha() else action[::-1].upper()
            row, col = parse_input(coord)
            # Check that square is not already filled.
            if board[row][col] != 0:
                print(f"ERROR: Square {coord} is filled.")
            else:
                display_board(board, row, col)
                action = input(f"What is the value at `{coord}`?: ")

                # Show possible values at coordinate.
                if action.lower() == "s":
                    valid_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                    for key in get_illegal_moves(board, row, col).keys():
                        if key in valid_values:
                            valid_values.remove(key)
                    print(f"INFO: Possible values are {valid_values}.")
                    action = input(f"What is the value at `{coord}`?: ")

                try:
                    number = int(action)
                    if not (1 <= number <= 9):
                        raise ValueError
                    invalid_moves = get_illegal_moves(board, row, col)
                    if number not in invalid_moves.keys():
                        action_taken = True
                        board[row][col] = number
                    else:
                        print(f"ERROR: {number} is already present in", end="")
                        if "ROW" in invalid_moves[number]:
                            print(f" - row {coord[-1]}", end="")
                        if "COL" in invalid_moves[number]:
                            print(f" - column {coord[0]}", end="")
                        if "BOX" in invalid_moves[number]:
                            print(f" - current 3x3 box", end="")
                        print(".")
                except ValueError:
                    print(f"ERROR: The value `{action}` is invalid.")
        # Not quitting or editing a valid square.
        else:
            print(f"ERROR: Square `{action}` is invalid.")
    return False


def main():
    """Program main."""
    board = read_board()
    done = False
    while not done:
        done = play_round(board)


if __name__ == "__main__":
    main()
