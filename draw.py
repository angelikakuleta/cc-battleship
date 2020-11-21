import settings as sett

pygame = sett.pygame
screen = sett.screen


def draw_boards(boards, players, is_left_visible):
    screen.fill(sett.COLORS["BGR"])
    draw_board(players[0]["name"], True)
    draw_board(players[1]["name"], False)
    draw_ships(boards[0], True, is_left_visible)
    draw_ships(boards[1], False, not is_left_visible)


def draw_board(player_name, is_left):

    x_start = sett.BOARDS_X[0] if is_left else sett.BOARDS_X[1]
    y_start = sett.BOARDS_Y[0] if is_left else sett.BOARDS_Y[1]

    x_end = sett.SIDE_LENGTH*sett.BOARD_SIZE + (sett.BOARD_BORDER % 2)*1 + x_start
    y_end = sett.SIDE_LENGTH*sett.BOARD_SIZE + (sett.BOARD_BORDER % 2)*1 + y_start

    pygame.draw.line(screen, sett.COLORS["LINE"], (x_start, y_start), (x_start, y_end+1), sett.BOARD_BORDER)
    pygame.draw.line(screen, sett.COLORS["LINE"], (x_start, y_start), (x_end+1, y_start), sett.BOARD_BORDER)
    pygame.draw.line(screen, sett.COLORS["LINE"], (x_start, y_end+1), (x_end+1, y_end+1), sett.BOARD_BORDER)
    pygame.draw.line(screen, sett.COLORS["LINE"], (x_end+1, y_start), (x_end+1, y_end+1), sett.BOARD_BORDER)

    x = x_start + sett.BOARD_BORDER % 2
    y = y_start + sett.BOARD_BORDER % 2

    for i in range(sett.BOARD_SIZE-1):
        x += sett.SIDE_LENGTH
        y += sett.SIDE_LENGTH
        pygame.draw.line(screen, sett.COLORS["LINE"], (x, y_start), (x, y_end))
        pygame.draw.line(screen, sett.COLORS["LINE"], (x_start, y), (x_end, y))

    draw_numbers(x_start + sett.SIDE_LENGTH*0.5, y_start - sett.SIDE_LENGTH)
    draw_letters(x_start - sett.SIDE_LENGTH*0.5, y_start+sett.SIDE_LENGTH*0.5)
    draw_player_name(x_start + ((x_end - x_start) / 2), y_end, player_name)


def draw_numbers(pos_x, pos_y):
    for n in range(1, sett.BOARD_SIZE+1):
        font = pygame.font.SysFont("Arial", int(sett.SIDE_LENGTH/2))
        text = font.render(str(n), 1, sett.COLORS["TEXT_MENU"])
        screen.blit(text, (pos_x - (text.get_width()/2), pos_y + (sett.SIDE_LENGTH/4)))
        pos_x += sett.SIDE_LENGTH


def draw_letters(pos_x, pos_y):
    letters = "ABCDEFGHIJ"
    for i in range(sett.BOARD_SIZE):
        font = pygame.font.SysFont("Arial", int(sett.SIDE_LENGTH/2))
        text = font.render(letters[i], 1, sett.COLORS["TEXT_MENU"])
        screen.blit(text, (pos_x - (text.get_width()/2), pos_y - (sett.SIDE_LENGTH/4)))
        pos_y += sett.SIDE_LENGTH


def draw_player_name(pos_x, pos_y, name):
    font = pygame.font.SysFont("Arial", int(sett.SIDE_LENGTH/2))
    text = font.render(name, 1, sett.COLORS["TEXT_MENU"])
    screen.blit(text, (pos_x - (text.get_width()/2), pos_y + (sett.SIDE_LENGTH/4)))


def draw_ships(board, is_left, is_visible):
    for row in range(len(board)):
        for col in range(len(board)):
            draw_ship((row, col), board[row][col], is_left, is_visible)


def draw_ship(pos, sign, is_left, is_visible=True):
    gap = sett.SIDE_LENGTH
    index = 0 if is_left else 1
    start_x = sett.BOARDS_X[index] + sett.BOARD_BORDER % 2 + 1
    start_Y = sett.BOARDS_Y[index] + sett.BOARD_BORDER % 2 + 1

    color = sett.COLORS["EMPTY"]
    if sign == "M":
        color = sett.COLORS["MISS"]
    elif sign == "H":
        color = sett.COLORS["HIT"]
    elif sign == "S":
        color = sett.COLORS["SINK"]
    elif sign == "X" and is_visible:
        color = sett.COLORS["SHIP"]

    field_x = start_x + gap * pos[1]
    field_y = start_Y + gap * pos[0]
    pygame.draw.rect(screen, color, (field_x, field_y, gap-1, gap-1))


def draw_initialization_state(player, board):
    screen.fill(sett.COLORS["BGR"])
    draw_board(player["name"], player["is_left"])
    draw_ships(board, player["is_left"], is_visible=True)


def draw_initialization_info(size, is_left):
    font = pygame.font.SysFont("Arial", int(sett.SIDE_LENGTH / 2))
    text = font.render(f"Put a {size}-masted ship", True, sett.COLORS["TEXT_MENU"], sett.COLORS["BGR"])
    index = 1 if is_left else 0
    x = sett.BOARDS_X[index] + (sett.BOARD_SIZE*sett.SIDE_LENGTH / 2)
    y = sett.BOARDS_Y[index] + (sett.BOARD_SIZE*sett.SIDE_LENGTH / 2)
    screen.blit(text, (x-text.get_width() / 2,  y - text.get_height()/2))
