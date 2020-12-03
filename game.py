from random import randint
import draw
from settings import SHIP_SIZES


def init_board(size):
    """Returns an empty board (with 0)."""
    board = []
    for i in range(size):
        board.append([])
        for j in range(size):
            board[i].append("0")
    return board


def get_avaliable_fields(board_size, free_fields, ship):
    avaliable_fields = set()
    for (row, col) in ship:
        if (row > 0 and (row-1, col) in free_fields and (row-1, col) not in ship):
            avaliable_fields.add((row-1, col))
        if (row < board_size-1 and (row+1, col) in free_fields and (row+1, col) not in ship):
            avaliable_fields.add((row+1, col))
        if (col > 0 and (row, col-1) in free_fields and (row, col-1) not in ship):
            avaliable_fields.add((row, col-1))
        if (col < board_size-1 and (row, col+1) in free_fields and (row, col+1) not in ship):
            avaliable_fields.add((row, col+1))
    return list(avaliable_fields)


def place_ships_automatically(board, ship_sizes=SHIP_SIZES):
    ships = []
    free_fields = [(row, col) for row in range(len(board)) for col in range(len(board))]

    i = 0
    while i < len(ship_sizes):
        size = ship_sizes[i]
        ship = []

        ship.append(free_fields[randint(0, len(free_fields)-1)])

        is_placement_possible = True
        for j in range(size-1):
            avaliable_fields = get_avaliable_fields(len(board), free_fields, ship)
            if len(avaliable_fields) > 0:
                ship.append(avaliable_fields[randint(0, len(avaliable_fields)-1)])
            else:
                is_placement_possible = False
                break

        if is_placement_possible:
            ships.append(ship)
            for pos in ship:
                free_fields.remove(pos)
            for pos in get_avaliable_fields(len(board), free_fields, ship):
                free_fields.remove(pos)
            i += 1

    for x in ships:
        for pos in x:
            board[pos[0]][pos[1]] = "X"

    return ships


def is_valid_move(board, pos):
    row, col = pos
    if board[row][col] not in "MHS":
        return True
    else:
        return False


def mark(board, ships, pos, is_left):
    row, col = pos

    if board[row][col] == "0":
        board[row][col] = "M"
        draw.draw_ship(pos, "M", is_left)
    elif board[row][col] == "X":
        if is_ship_sunken(board, ships, pos):
            ship = sink(board, ships, pos)
            for pos in ship:
                draw.draw_ship(pos, "S", is_left)
        else:
            board[row][col] = "H"
            draw.draw_ship(pos, "H", is_left)


def is_ship_sunken(board, ships, pos):
    for ship in ships:
        if pos in ship:
            for x in ship:
                if x != pos and board[x[0]][x[1]] == "X":
                    return False
    return True


def sink(board,  ships, pos):
    for ship in ships:
        if pos in ship:
            for x in ship:
                board[x[0]][x[1]] = "S"
            return ship


def get_computer_move(board):
    '''Returns some move for the computer agent using the Hunt/Target algorithm'''
    targets = get_targets(board)
    if targets:
        return targets[randint(0, len(targets)-1)]
    else:
        avaliable_moves = get_avaliable_moves(board)
        return avaliable_moves[randint(0, len(avaliable_moves)-1)]


def get_targets(board):
    hit_fields = []
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == "H":
                hit_fields.append((row, col))

    targets = []
    for (row, col) in hit_fields:
        if row > 0 and is_collision_free_move(board, (row-1, col)):
            targets.append((row-1, col))
        if row < len(board)-1 and is_collision_free_move(board, (row+1, col)):
            targets.append((row+1, col))
        if col > 0 and is_collision_free_move(board, (row, col-1)):
            targets.append((row, col-1))
        if col < len(board)-1 and is_collision_free_move(board, (row, col+1)):
            targets.append((row, col+1))
    return targets


def get_avaliable_moves(board):
    avaliable_moves = []
    for row in range(len(board)):
        for col in range(len(board)):
            if is_collision_free_move(board, (row, col)):
                avaliable_moves.append((row, col))
    return avaliable_moves


def is_collision_free_move(board, pos):
    if not is_valid_move(board, pos):
        return False

    row, col = pos
    if row > 0 and board[row-1][col] == "S":
        return False
    if row < len(board)-1 and board[row+1][col] == "S":
        return False
    if col > 0 and board[row][col-1] == "S":
        return False
    if col < len(board)-1 and board[row][col+1] == "S":
        return False

    return True


def is_all_sunken(board):
    """Returns True if player has sunk all enemy ships."""
    for row in board:
        if "X" in row or "H" in row:
            return False
    return True
