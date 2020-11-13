def init_board(size):
    """Returns an empty board (with 0)."""
    board = []
    for i in range(size):
        board.append([])
        for j in range(size):
            board[i].append("0")
    return board


def print_board(board, player, visible=True):
    print(f"Player {player}")
    letters = "ABCDEFGHIJ"
    print(" ", end="")
    for i in range(len(board)):
        print(f" {i+1}", end="")
    print()
    for i in range(len(board)):
        for j in range(-1, len(board)):
            if (j == -1):
                print(letters[i], end="")
            else:
                sign = board[i][j]
                if not visible and sign == "X":
                    sign = "0"
                print(f" {sign}", end="")
        print()
    print()


def place_the_ships(board):
    player_ships = []
    player_ships.append([(1, 0), (1, 1)])
    player_ships.append([(3, 1), (4, 1)])
    player_ships.append([(0, 4)])
    player_ships.append([(2, 3)])
    player_ships.append([(4, 4)])

    for ship in player_ships:
        for coords in ship:
            board[coords[0]][coords[1]] = "X"

    return player_ships


def is_all_sunken(board):
    """Returns True if player has sunk all enemy ships."""
    for row in board:
        if "X" in row or "H" in row:
            return False
    return True


def is_ship_sunken(board, player_ships, coords):
    for ship in player_ships:
        if coords in ship:
            for x in ship:
                if x != coords and board[x[0]][x[1]] == "X":
                    return False
    return True


def sink(board,  player_ships, coords):
    for ship in player_ships:
        if coords in ship:
            for x in ship:
                board[x[0]][x[1]] = "S"


def mark(board, player_ships, coords):
    row = coords[0]
    col = coords[1]

    if board[row][col] == "0":
        board[row][col] = "M"
    elif board[row][col] == "X":
        if is_ship_sunken(board, player_ships, coords):
            sink(board, player_ships, coords)
        else:
            board[row][col] = "H"


def is_valid_move(board, coords):
    row = coords[0]
    col = coords[1]
    if board[row][col] not in ["M", "H", "S"]:
        return True
    else:
        return False


def human_human_mode(boards):
    ships = [None, None]
    player = 1
    opponent = 2
    winner = None

    ships[player-1] = place_the_ships(boards[player-1])
    ships[opponent-1] = place_the_ships(boards[opponent-1])

    while not winner:
        valid_move = False

        print_board(boards[player-1], player)
        print_board(boards[opponent-1], opponent, False)

        while not valid_move:
            move = input("Type the board coordinates: ").upper()
            coords = ("ABCDEFGHIJ".index(move[0]), int(move[1])-1)
            if is_valid_move(boards[opponent-1], coords):
                mark(boards[opponent-1], ships[opponent-1], coords)
                valid_move = True

        print_board(boards[player-1], player)
        print_board(boards[opponent-1], opponent, False)

        input("Press any key to continue...")

        if is_all_sunken(boards[opponent-1]):
            winner = player
        else:
            player = opponent
            opponent = 2 if player == 1 else 1

    print(f"Player {player} win!")


def battleship_game(mode="HUMAN-HUMAN", board_size=5):
    boards = [None, None]
    boards[0] = init_board(board_size)
    boards[1] = init_board(board_size)

    if mode == "HUMAN-HUMAN":
        human_human_mode(boards)


def main_menu():
    # board_size = 5
    battleship_game()


if __name__ == '__main__':
    main_menu()
