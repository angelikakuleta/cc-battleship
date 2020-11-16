import pygame
import time

width = 1450
height = 870
pygame.init()
pygame.font.init()
pygame.display.set_caption("Cool Battleships")    
screen = pygame.display.set_mode((width, height))
screen.fill((135,206,250))
FPS = 30                          

numbers_list = ("1","2","3","4","5","6","7","8","9","10")
alphabet_list = ("A","B","C","D","E","F","G","H","I","J")


def player_one_box(screen):
    rows = 10
    x = 55
    y = 55
    divide = 65

    for i in range(rows):
        x += divide
        y += divide
        pygame.draw.line(screen,(0,0,0),(x,55),(x,705))
        pygame.draw.line(screen,(0,0,0),(55,y),(705,y))

        pygame.draw.line(screen,(0,0,0),(55,55),(55,705),3)
        pygame.draw.line(screen,(0,0,0),(55,55),(705,55),3)
        pygame.draw.line(screen,(0,0,0),(55,705),(705,705),3)
        pygame.draw.line(screen,(0,0,0),(705,55),(705,705),3)
    
    drawnumbers(87.5,screen)
    drawstring(87.5,screen)
    pygame.display.update()


def player_two_box(screen):
    rows = 10
    x = 730
    y = 55
    divide = 65

    for i in range(rows):
        x += divide
        y += divide
        pygame.draw.line(screen,(0,0,0),(x,55),(x,705))
        pygame.draw.line(screen,(0,0,0),(730,y),(1380,y))

        pygame.draw.line(screen,(0,0,0),(730,55),(730,705),3)
        pygame.draw.line(screen,(0,0,0),(730,55),(1380,55),3)
        pygame.draw.line(screen,(0,0,0),(730,705),(1380,705),3)
        pygame.draw.line(screen,(0,0,0),(1380,55),(1380,705),3)
    
    drawnumbers(765,screen)
    pygame.display.update()


def drawnumbers(pos, screen):
    for b in numbers_list:
        font = pygame.font.SysFont('arial',25)
        text = font.render(b,1,(0,0,0))
        screen.blit(text,(pos - (text.get_width()/2),5))
        pos += 65


def drawstring(pos, screen):
    for i in alphabet_list:
        font = pygame.font.SysFont('arial',25)
        text = font.render(i,1,(0,0,0))
        screen.blit(text,(5,pos - (text.get_width()/2)))
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
                if pos[0] >= 730 and pos[0] < 1380 and pos[1] >= 55 and pos[1] < 705:
                    return pos

def ship_drawing(coordinates, sign, side):
    width = 65
    color = (0, 0, 0)
    x_start = 55 if side == "L" else 730
    y_start = 55
    
    if side == "R" and sign == "X":
        pass
    else:
        if sign == "S":
            color = (255, 0, 0)
        elif sign == "M":
            pass

        pygame.draw.rect(screen, color,(x_start+width*coordinates[0], y_start+width*coordinates[1],width,width))
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
                ship_drawing((row, col), board[row][col], side)


def get_coords(move):
    print(move)
    x = int((move[0] - 730) / 65)
    y = int((move[1] - 55) / 65)
    return (x, y)


def is_valid_move(board, coords):
    row = coords[0]
    col = coords[1]
    if board[row][col] not in ["M", "H", "S"]:
        return True
    else:
        return False


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
    # TODO: Sink the ship (GUI)


def human_human_mode(boards):
    ships = [None, None]
    player = 1
    opponent = 2
    winner = None
    run = True
    clock = pygame.time.Clock()
    
    ships[player-1] = place_the_ships(boards[player-1])
    ships[opponent-1] = place_the_ships(boards[opponent-1])

    while run:
        clock.tick(FPS)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        valid_move = False

        # clean
        screen.fill((135,206,250))
        player_one_box(screen)
        player_two_box(screen)

        draw_board(boards[player-1], "L")
        draw_board(boards[opponent-1], "R")

        player_text = "One" if player == 1 else "Two"
        font = pygame.font.SysFont('arial',100)
        text = font.render(f"Player {player_text}",5,(0,0,0))
        screen.blit(text,(380-text.get_width()/2,730))

        opponent_text = "One" if opponent == 1 else "Two"
        font = pygame.font.SysFont('arial',100)
        text = font.render(f"Player {opponent_text}",5,(0,0,0))
        screen.blit(text,(1050-text.get_width()/2,730))

        pygame.display.update()

        while not valid_move:
            move = get_move()
            coords = get_coords(move)
            if is_valid_move(boards[opponent-1], coords):
                mark(boards[opponent-1], ships[opponent-1], coords)
                ship_drawing(coords, boards[opponent-1][coords[0]][coords[1]], "R")
                valid_move = True

        input("press something") # to delete

        if is_all_sunken(boards[opponent-1]):
            winner = player
            # TODO: Display information that the player wins (GUI)
            # TODO: Add restart game to menu, exit on ESC key
        else:
            player = opponent
            opponent = 2 if player == 1 else 1
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

    run = True
    clock = pygame.time.Clock()

    if mode == "HUMAN-HUMAN":
        human_human_mode(boards)


def main():
    player_one_box(screen)
    player_two_box(screen)
    battleship_game()


if __name__ == '__main__':
    main()

