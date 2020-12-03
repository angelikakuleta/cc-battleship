import pygame

WIDTH = 960
HEIGHT = 520

MENU_WIDTH = WIDTH * 0.8
MENU_HIGHT = HEIGHT * 0.8

COLORS = {
    "BGR": (40, 41, 35),
    "BGR_MENU": (128, 0, 128),
    "TEXT_MENU": (255, 255, 255),
    "LINE": (0, 0, 0),
    "EMPTY": (255, 255, 255),
    "SHIP": (128, 0, 128),
    "MISS": (72, 100, 135),
    "HIT": (248, 226, 110),
    "SINK": (225, 113, 82),
}

BOARD_SIZE = 8
SHIP_SIZES = [5, 4, 4, 3, 2]

BOARD_BORDER = 3

SIDE_LENGTH = HEIGHT//(BOARD_SIZE+3)
BOARDS_X = [SIDE_LENGTH*1.5, SIDE_LENGTH*(BOARD_SIZE+3)]
BOARDS_Y = [SIDE_LENGTH*1.5, SIDE_LENGTH*1.5]

pygame.init()
pygame.display.set_caption("Cool Battleships")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
