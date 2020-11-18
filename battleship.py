import pygame
from random import randint
import pygame_menu

WIDTH = 920
HEIGHT = 500
COLORS = {
    "BGR": (160, 196, 227),
    "SHIP": (35, 59, 55),
    "MISS": (72, 100, 135),
    "HIT": (248, 226, 110),
    "SINK": (225, 113, 82)
}

pygame.init()
pygame.font.init()
pygame.display.set_caption("Cool Battleships")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(COLORS["BGR"])
FPS = 30


#menu options
def start_game_options():
    pass

def main_menu():
    menu = pygame_menu.Menu(500, 920, "Main menu", theme = pygame_menu.themes.THEME_BLUE)

    menu.add_selector("Mode:", [("Human vs Human", 1), ("Human vs AI", 2), ("AI vs AI", 3)])
    menu.add_button("Start", start_game_options)
    menu.add_button("Quit", pygame_menu.events.EXIT)
    menu.mainloop(screen)

main_menu()



def player_one_box(screen, board_size):
    rows = 11
    side_length = 40
    x = side_length
    y = side_length

    for i in range(rows - 1):
        x += side_length
        y += side_length
        pygame.draw.line(screen, (0, 0, 0), (x, side_length), (x, side_length * rows))
        pygame.draw.line(screen, (0, 0, 0), (side_length, y), (side_length * rows, y))

    pygame.draw.line(screen, (0, 0, 0), (side_length, side_length), (side_length, side_length * rows), 3)
    pygame.draw.line(screen, (0, 0, 0), (side_length, side_length), (side_length * rows, side_length), 3)
    pygame.draw.line(screen, (0, 0, 0), (side_length, side_length * rows), (side_length * rows, side_length * rows), 3)
    pygame.draw.line(screen, (0, 0, 0), (side_length * rows, side_length), (side_length * rows, side_length * rows), 3)

    draw_numbers(60, screen)
    draw_string(50, screen)
    pygame.display.update()


def player_two_box(screen, board_size):
    rows = 11
    side_length = 40
    x = side_length + 400
    y = side_length

    for i in range(rows - 1):
        x += side_length
        y += side_length
        pygame.draw.line(screen, (0, 0, 0), (x, side_length), (x, side_length * rows))
        pygame.draw.line(screen, (0, 0, 0), (side_length * 12, y), (side_length * 22, y))

    pygame.draw.line(screen, (0, 0, 0), (side_length * 12, side_length), (side_length * 12, side_length * 11), 3)
    pygame.draw.line(screen, (0, 0, 0), (side_length * 12, side_length), (side_length * 22, side_length), 3)
    pygame.draw.line(screen, (0, 0, 0), (side_length * 12, side_length * 11), (side_length * 22, side_length * 11), 3)
    pygame.draw.line(screen, (0, 0, 0), (side_length * 22, side_length), (side_length * 22, side_length * 11), 3)

    draw_numbers(side_length * 12.5, screen)
    pygame.display.update()


def draw_numbers(pos, screen):
    for n in range(1, 11):
        font = pygame.font.SysFont("Arial", 25)
        text = font.render(str(n), 1, (0, 0, 0))
        screen.blit(text, (pos - (text.get_width()/2), 5))
        pos += 40


def draw_string(pos, screen):
    for ch in "ABCDEFGHIJ":
        font = pygame.font.SysFont("Arial", 25)
        text = font.render(ch, 1, (0, 0, 0))
        screen.blit(text, (5, pos - (text.get_width()/2)))
        pos += 40


def get_move():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] >= 481 and pos[0] < 881 and pos[1] >= 41 and pos[1] < 441:
                    return get_coords(pos)


def draw_ship(coords, sign, side):
    gap = 40
    board_x = 41 if side == "L" else 481
    board_y = 41

    color = COLORS["SHIP"]
    if sign == "M":
        color = COLORS["MISS"]
    elif sign == "H":
        color = COLORS["HIT"]
    elif sign == "S":
        color = COLORS["SINK"]

    if not (side == "R" and sign == "X"):
        field_x = board_x + gap * coords[1]
        field_y = board_y + gap * coords[0]
        pygame.draw.rect(screen, color, (field_x, field_y, gap-1, gap-1))
        pygame.display.update()


def place_the_ships(board):
    # TODO: Ask player about ship positioning with validation
    player_ships = [
        [(3, 2), (4, 2), (4, 3), (5, 2), (6, 2)],
        [(6, 8), (6, 7), (7, 8), (6, 9)],
        [(9, 2), (9, 1), (9, 0), (9, 3)],
        [(3, 7), (4, 7), (2, 7)],
        [(5, 0), (4, 0)]
    ]

    for ship in player_ships:
        for coords in ship:
            board[coords[0]][coords[1]] = "X"

    return player_ships



def get_avaliable_fields(board_size, free_fields, ship):
    avaliable_fields = set()
    for (row, col) in ship:
        if (row > 0 and (row-1, col) in free_fields and (row-1, col) not in ship):
            avaliable_fields.add((row-1, col))
        if (row < board_size-1 and (row+1, col) in free_fields and (row+1, col) not in ship):
            avaliable_fields.add((row+1, col))
        if (col > 0 and (row, col+1) in free_fields and (row, col+1) not in ship):
            avaliable_fields.add((row, col+1))
        if (col < board_size-1 and (row, col-1) in free_fields and (row, col-1) not in ship):
            avaliable_fields.add((row, col-1))
    return list(avaliable_fields)


def place_the_ships_automatically(board, ship_sizes=[5, 4, 4, 3, 2]):
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
            for coords in ship:
                free_fields.remove(coords)
            for coords in get_avaliable_fields(len(board), free_fields, ship):
                free_fields.remove(coords)
            i += 1

    for x in ships:
        for coords in x:
            board[coords[0]][coords[1]] = "X"

    return ships


def draw_board(board, side):
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] in "XMHS":
                draw_ship((row, col), board[row][col], side)


def get_coords(move):
    row = (move[1] - 41) // 40
    col = (move[0] - 481) // 40
    return (row, col)


def is_valid_move(board, coords):
    row, col = coords
    if board[row][col] not in "MHS":
        return True
    else:
        return False


def is_collision_free_move(board, coords):
    if not is_valid_move(board, coords):
        return False

    row, col = coords
    if row > 0 and board[row-1][col] == "S":
        return False
    if row < len(board)-1 and board[row+1][col] == "S":
        return False
    if col > 0 and board[row][col-1] == "S":
        return False
    if col < len(board)-1 and board[row][col+1] == "S":
        return False

    return True


def mark(board, player_ships, coords, side="R"):
    row, col = coords

    if board[row][col] == "0":
        board[row][col] = "M"
        draw_ship(coords, "M", side)
    elif board[row][col] == "X":
        if is_ship_sunken(board, player_ships, coords):
            ship = sink(board, player_ships, coords)
            for coords in ship:
                draw_ship(coords, "S", side)
        else:
            board[row][col] = "H"
            draw_ship(coords, "H", side)


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
            return ship


def redraw_screen(boards, board_size, player):
    opponent = 2 if player == 1 else 1

    screen.fill(COLORS["BGR"])
    player_one_box(screen, board_size)
    player_two_box(screen, board_size)

    draw_board(boards[player-1], "L")
    draw_board(boards[opponent-1], "R")

    player_text = "One" if player == 1 else "Two"
    font = pygame.font.SysFont("Arial", 50)
    text = font.render(f"Player {player_text}", 5, (0, 0, 0))
    screen.blit(text, (240-text.get_width() / 2, 440))

    opponent_text = "One" if opponent == 1 else "Two"
    font = pygame.font.SysFont("Arial", 50)
    text = font.render(f"Player {opponent_text}", 5, (0, 0, 0))
    screen.blit(text, (680-text.get_width() / 2, 440))

    pygame.display.update()


def human_human_mode(boards, board_size):
    ships = [None, None]
    player = 1
    opponent = 2 if player == 1 else 1
    run = True
    clock = pygame.time.Clock()
    current_time, end_time = 0, 0

    ships[player-1] = place_the_ships(boards[player-1])
    ships[opponent-1] = place_the_ships(boards[opponent-1])

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        current_time = pygame.time.get_ticks()
        if current_time >= end_time:
            redraw_screen(boards, board_size, player)
            valid_move = False
            while not valid_move:
                move = get_move()
                if is_valid_move(boards[opponent-1], move):
                    mark(boards[opponent-1], ships[opponent-1], move)
                    valid_move = True

            if is_all_sunken(boards[opponent-1]):
                # TODO: Display information that the player wins (GUI)
                # TODO: Add restart game to menu, exit on ESC key
                pass
            else:
                player = opponent
                opponent = 2 if player == 1 else 1
                current_time = pygame.time.get_ticks()
                end_time = pygame.time.get_ticks() + 2000

                # TODO: Display player change window

    pygame.quit()


def get_targets(board):
    hit_fields = []
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == "H":
                hit_fields.append((row, col))

    targets = []
    for (row, col) in hit_fields:
        if (is_collision_free_move(board, (row-1, col)) and row > 0):
            targets.append((row-1, col))
        if (is_collision_free_move(board, (row+1, col)) and row < len(board)-1):
            targets.append((row+1, col))
        if (is_collision_free_move(board, (row, col-1)) and col > 0):
            targets.append((row, col-1))
        if (is_collision_free_move(board, (row, col+1)) and col < len(board)-1):
            targets.append((row, col+1))
    return targets


def get_avaliable_moves(board):
    avaliable_moves = []
    for row in range(len(board)):
        for col in range(len(board)):
            if is_collision_free_move(board, (row, col)):
                avaliable_moves.append((row, col))
    return avaliable_moves


def get_computer_move(board):
    # Hunt/Target algorithm
    targets = get_targets(board)
    if targets:
        return targets[randint(0, len(targets)-1)]
    else:
        avaliable_moves = get_avaliable_moves(board)
        return avaliable_moves[randint(0, len(avaliable_moves)-1)]


def human_computer_mode(boards, board_size):
    ships = [None, None]
    player = 1
    computer = 2
    run = True
    clock = pygame.time.Clock()
    current_time, end_time = 0, 0

    ships[player-1] = place_the_ships(boards[player-1])
    ships[computer-1] = place_the_ships_automatically(boards[computer-1])

    redraw_screen(boards, board_size, player)

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if (player != computer):
            valid_move = False
            while not valid_move:
                move = get_move()
                if is_valid_move(boards[1], move):
                    mark(boards[1], ships[1], move, "R")
                    valid_move = True
        else:
            current_time = pygame.time.get_ticks()
            end_time = pygame.time.get_ticks() + 2000
            while current_time < end_time:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                current_time = pygame.time.get_ticks()
            move = get_computer_move(boards[0])
            mark(boards[0], ships[0], move, "L")

        if is_all_sunken(boards[computer-1]):
            # TODO: Display information that the player wins (GUI)
            # TODO: Add restart game to menu, exit on ESC key
            pass
        else:
            player = 2 if player == 1 else 1

            # TODO: Display player change window

    pygame.quit()


def init_board(size):
    """Returns an empty board (with 0)."""
    board = []
    for i in range(size):
        board.append([])
        for j in range(size):
            board[i].append("0")
    return board


def battleship_game(mode="HUMAN-HUMAN", board_size=10):
    boards = [None, None]
    boards[0] = init_board(board_size)
    boards[1] = init_board(board_size)

    player_one_box(screen, board_size)
    player_two_box(screen, board_size)

    if mode == "HUMAN-HUMAN":
        human_human_mode(boards, board_size)
    elif mode == "HUMAN-COMPUTER":
        human_computer_mode(boards, board_size)


def main():
    battleship_game("HUMAN-COMPUTER")


if __name__ == '__main__':
    main()
