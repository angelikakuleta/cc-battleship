import pygame

WIDTH = 1450
HEIGHT = 870
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


def player_one_box(screen, board_size):
    board_border = 3
    x = 55 + board_border // 2
    y = 55 + board_border // 2
    divide = 65

    for i in range(board_size-1):
        x += divide
        y += divide
        pygame.draw.line(screen, (0, 0, 0), (x, 55), (x, 705))
        pygame.draw.line(screen, (0, 0, 0), (55, y), (705, y))

    pygame.draw.line(screen, (0, 0, 0), (55, 55), (55, 705), board_border)
    pygame.draw.line(screen, (0, 0, 0), (55, 55), (705, 55), board_border)
    pygame.draw.line(screen, (0, 0, 0), (55, 705), (705, 705), board_border)
    pygame.draw.line(screen, (0, 0, 0), (705, 55), (705, 705), board_border)

    draw_numbers(87.5, screen)
    draw_string(87.5, screen)
    pygame.display.update()


def player_two_box(screen, board_size):
    board_border = 3
    x = 730 + board_border // 2
    y = 55 + board_border // 2
    gap = 65

    for i in range(board_size-1):
        x += gap
        y += gap
        pygame.draw.line(screen, (0, 0, 0), (x, 55), (x, 705))
        pygame.draw.line(screen, (0, 0, 0), (730, y), (1380, y))

    pygame.draw.line(screen, (0, 0, 0), (730, 55), (730, 705), board_border)
    pygame.draw.line(screen, (0, 0, 0), (730, 55), (1380, 55), board_border)
    pygame.draw.line(screen, (0, 0, 0), (730, 705), (1380, 705), board_border)
    pygame.draw.line(screen, (0, 0, 0), (1380, 55), (1380, 705), board_border)

    draw_numbers(765, screen)
    pygame.display.update()


def draw_numbers(pos, screen):
    for n in range(1, 11):
        font = pygame.font.SysFont("Arial", 25)
        text = font.render(str(n), 1, (0, 0, 0))
        screen.blit(text, (pos - (text.get_width()/2), 5))
        pos += 65


def draw_string(pos, screen):
    for ch in "ABCDEFGHIJ":
        font = pygame.font.SysFont("Arial", 25)
        text = font.render(ch, 1, (0, 0, 0))
        screen.blit(text, (5, pos - (text.get_width()/2)))
        pos += 65


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
                if pos[0] >= 731 and pos[0] < 1381 and pos[1] >= 56 and pos[1] < 706:
                    return pos


def draw_ship(coords, sign, side):
    gap = 65
    board_x = 57 if side == "L" else 732
    board_y = 57

    color = COLORS["SHIP"]
    if sign == "M":
        color = COLORS["MISS"]
    elif sign == "H":
        color = COLORS["HIT"]
    elif sign == "S":
        color = COLORS["SINK"]

    if not (side == "R" and sign == "X"):
        field_x = board_x + gap * coords[0]
        field_y = board_y + gap * coords[1]
        pygame.draw.rect(screen, color, (field_x, field_y, gap-1, gap-1))
        pygame.display.update()


def place_the_ships(board):
    # TODO: Ask player about ship positioning with validation
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


def draw_board(board, side):
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] in "XMHS":
                draw_ship((row, col), board[row][col], side)


def get_coords(move):
    print(move)

    x = int((move[0] - 731) / 65)
    y = int((move[1] - 56) / 65)
    return (x, y)


def is_valid_move(board, coords):
    row, col = coords
    if board[row][col] not in "MHS":
        return True
    else:
        return False


def mark(board, player_ships, coords):
    row, col = coords

    if board[row][col] == "0":
        board[row][col] = "M"
        draw_ship(coords, "M", "R")
    elif board[row][col] == "X":
        if is_ship_sunken(board, player_ships, coords):
            ship = sink(board, player_ships, coords)
            for coords in ship:
                draw_ship(coords, "S", "R")
        else:
            board[row][col] = "H"
            draw_ship(coords, "H", "R")


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
    font = pygame.font.SysFont("Arial", 100)
    text = font.render(f"Player {player_text}", 5, (0, 0, 0))
    screen.blit(text, (380-text.get_width() / 2, 730))

    opponent_text = "One" if opponent == 1 else "Two"
    font = pygame.font.SysFont("Arial", 100)
    text = font.render(f"Player {opponent_text}", 5, (0, 0, 0))
    screen.blit(text, (1050-text.get_width() / 2, 730))

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
                coords = get_coords(move)
                if is_valid_move(boards[opponent-1], coords):
                    mark(boards[opponent-1], ships[opponent-1], coords)
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


def main():
    battleship_game()


if __name__ == '__main__':
    main()
