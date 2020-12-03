import sys
import pygame_menu
import settings as sett
import game
import draw

pygame = sett.pygame
screen = sett.screen
clock = pygame.time.Clock()

main_menu = None
panel = None

initialized = False
game_on = False
game_mode = "HUMAN-HUMAN"
boards = [None, None]
ships = [None, None]
players = []
game_state = None
player = 0


def set_mode(mode, value):
    global game_mode, game_state

    if not game_state:
        if value == 1:
            game_mode = "HUMAN-HUMAN"
        elif value == 2:
            game_mode = "HUMAN-AI"


def change_view():
    global game_on

    game_on = True
    main_menu.disable()
    panel.disable()

    if game_state == "initialization":
        draw.draw_initialization_state(players[player], boards[player])
    elif game_state == "game":
        draw.draw_boards(boards, players, is_left_visible=players[player]["is_left"])
    pygame.display.update()


def get_menu():
    theme = pygame_menu.themes.THEME_DARK

    menu = pygame_menu.Menu(
        sett.MENU_HIGHT,
        sett.MENU_WIDTH,
        "Main menu",
        theme=theme,
        onclose=change_view
    )

    menu.add_selector("Mode: ", [("Human vs Human", 1), ("Human vs AI", 2)], onchange=set_mode)
    menu.add_button("Start", change_view)
    menu.add_button("Quit", pygame_menu.events.EXIT)
    menu.add_label("")
    menu.add_label("You can quit game while it's running by pressing an ESC key", font_size=20, font_color=sett.COLORS["TEXT_MENU"])
    menu.add_label("Pressing a \"S\" key anytime bring You back to the menu!", font_size=20, font_color=sett.COLORS["TEXT_MENU"])

    return menu


def get_panel():
    theme = pygame_menu.themes.THEME_DARK

    menu = pygame_menu.Menu(
        sett.MENU_HIGHT,
        sett.MENU_WIDTH,
        "Information",
        theme=theme,
        onclose=change_view
    )

    menu.add_button("Continue", change_view)
    menu.add_button("Quit", pygame_menu.events.EXIT)
    menu.add_label("")
    menu.add_label("Time to change players...", font_size=20, font_color=sett.COLORS["TEXT_MENU"])

    return menu


def init(events):
    global initialized, players, game_state, player, panel
    game_state = "initialization"

    print(f"{game_mode} mode running")

    if game_mode == "HUMAN-HUMAN":
        players = [
                    {"name": "Player 1", "is_left": True},
                    {"name": "Player 2", "is_left": False},
                  ]
    else:
        players = [
                    {"name": "Player", "is_left": True},
                    {"name": "Computer", "is_left": False},
                  ]

    boards[0] = game.init_board(sett.BOARD_SIZE)
    boards[1] = game.init_board(sett.BOARD_SIZE)

    player = 0
    ships[0] = place_ships(boards[0], players[0]["name"], is_left=players[0]["is_left"])
    wait(1000)

    player = 1

    if game_mode == "HUMAN-HUMAN":
        panel.enable()
        panel.mainloop(screen, bgfun=lambda: screen.fill(sett.COLORS["BGR_MENU"]))
        ships[1] = place_ships(boards[1], players[1]["name"], is_left=players[1]["is_left"])
        wait(1000)
    else:
        ships[1] = game.place_ships_automatically(boards[1])

    player = 0
    initialized = True


def get_move(is_left):
    action = None
    while not action or "coords" not in action:
        clock.tick(60 if game_on is False else 15)
        action = get_action()

    coords = action["coords"]
    x_start = sett.BOARDS_X[0] + 1 if is_left else sett.BOARDS_X[1]+1
    x_end = x_start + sett.BOARD_SIZE * sett.SIDE_LENGTH
    y_start = sett.BOARDS_Y[0] + 1 if is_left else sett.BOARDS_Y[1]+1
    y_end = y_start + sett.BOARD_SIZE * sett.SIDE_LENGTH

    if coords[0] >= x_start and coords[0] < x_end and coords[1] >= y_start and coords[1] < y_end:
        row = int((coords[1] - y_start) / sett.SIDE_LENGTH)
        col = int((coords[0] - x_start) / sett.SIDE_LENGTH)
        return (row, col)


def place_ships(board, player_name, is_left, ship_sizes=sett.SHIP_SIZES):
    player_ships = []
    free_fields = [(row, col) for row in range(len(board)) for col in range(len(board))]

    draw.draw_initialization_state(players[player], boards[player])
    pygame.display.update()

    i = 0
    while i < len(ship_sizes):
        size = ship_sizes[i]
        ship = []

        draw.draw_initialization_info(size, players[player]["is_left"])
        pygame.display.update()

        is_placement_possible = True
        for j in range(size):
            pos = get_move(is_left)

            if pos and len(ship) > 0:
                if pos in game.get_avaliable_fields(len(board), free_fields, ship):
                    ship.append(pos)
                    draw.draw_ship(pos, "X", is_left, is_visible=True)
                    pygame.display.update()
                else:
                    is_placement_possible = False
                    break
            elif pos in free_fields:
                ship.append(pos)
                draw.draw_ship(pos, "X", is_left, is_visible=True)
                pygame.display.update()
            else:
                is_placement_possible = False
                break

        if is_placement_possible:
            player_ships.append(ship)

            for pos in ship:
                board[pos[0]][pos[1]] = "X"

            for pos in ship:
                free_fields.remove(pos)
            for pos in game.get_avaliable_fields(len(board), free_fields, ship):
                free_fields.remove(pos)
            i += 1
        else:
            for pos in ship:
                draw.draw_ship(pos, "", is_left)
                pygame.display.update()

    return player_ships


def play():
    global player, game_state, game_on, initialized

    game_state = "game"
    run = True

    draw.draw_boards(boards, players, is_left_visible=players[player]["is_left"])
    pygame.display.update()

    while run:

        if game_mode == "HUMAN-HUMAN":
            draw.draw_boards(boards, players, is_left_visible=players[player]["is_left"])
            pygame.display.update()

        if game_mode == "HUMAN-HUMAN" or player == 0:
            valid_move = False
            while not valid_move:
                pos = get_move(not players[player]["is_left"])
                if pos and game.is_valid_move(boards[not player], pos):
                    game.mark(boards[not player], ships[not player], pos, not players[player]["is_left"])
                    pygame.display.update()
                    valid_move = True
        else:
            current_time = pygame.time.get_ticks()
            end_time = pygame.time.get_ticks() + 1000
            while current_time < end_time:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                current_time = pygame.time.get_ticks()
            pos = game.get_computer_move(boards[not player])
            game.mark(boards[not player], ships[not player], pos, not players[player]["is_left"])
            pygame.display.update()

        if game.is_all_sunken(boards[not player]):
            wait(1000)
            run = False
            game_state = None
            game_on = False
            initialized = False

            player_name = players[player]["name"]
            draw.draw_winner_info(player_name)
            pygame.display.update()

            action = None
            while not action or "menu" not in action:
                clock.tick(60 if game_on is False else 15)
                action = get_action()
        else:
            player = int(not player)
            if game_mode == "HUMAN-HUMAN":
                wait(1000)
                panel.enable()
                panel.mainloop(screen, bgfun=lambda: screen.fill(sett.COLORS["BGR_MENU"]))


def get_action():
    global main_menu, game_on
    events = pygame.event.get()

    for e in events:
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if e.key == pygame.K_s:
                main_menu.enable()
                game_on = False
                if not initialized:
                    return {"menu": True}
        elif e.type == pygame.MOUSEBUTTONDOWN:
            coords = pygame.mouse.get_pos()
            return {"coords": coords}

    if game_on is False:
        main_menu.mainloop(screen, bgfun=lambda: screen.fill(sett.COLORS["BGR_MENU"]))


def wait(ms):
    current_time = pygame.time.get_ticks()
    end_time = pygame.time.get_ticks() + ms
    while current_time < end_time:
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        current_time = pygame.time.get_ticks()


def main():
    global main_menu, panel, initialized, game_on

    main_menu = get_menu()
    panel = get_panel()

    # Main loop
    while True:
        clock.tick(60 if game_on is False else 15)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        if game_on is True:
            if initialized is False:
                init(events)

            play()
        else:
            main_menu.mainloop(screen, bgfun=lambda: screen.fill(sett.COLORS["BGR_MENU"]))

        pygame.display.flip()


if __name__ == '__main__':
    main()
