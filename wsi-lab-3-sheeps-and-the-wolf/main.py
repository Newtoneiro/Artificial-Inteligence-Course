import pygame
from constants import *
from components import Board
import time
import random
import sys
import argparse # sprawdzić dla depth i pokazac 7 ostatnich krokow

pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Wilk vs Owce")


def main(w_x: int, w_y: int, depth: int, w_r: bool, s_r: bool):
    run = True
    board = Board(WIN, WIDTH, HEIGHT, BOARD_SIZE, w_x, w_y, depth, w_r, s_r)

    seed = 0
    if not seed:
        seed = random.randrange(sys.maxsize)
    random.seed(seed)
    print(f"The seed is : {seed}")

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if board.update():
            run = False
        time.sleep(0.1)
    time.sleep(1)
    
    pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-Pos_x', '--WOLF_POSITION_X', type=int, required=True, help='X of Wolf\'s starting position')
    parser.add_argument('-Pos_y', '--WOLF_POSITION_Y', type=int, required=True, help='Y of Wolf\'s starting position')
    parser.add_argument('-D', '--DEPTH', type = int, help='Depth of minmax alghoritm')
    parser.add_argument('-WR', "--WOLF_RANDOM", action='store_true', required=False, help='Should wolf move randomly')
    parser.add_argument('-SR', "--SHEEP_RANDOM", action='store_true', required=False, help='Should sheeps move randomly')
    args = parser.parse_args()
    main(args.WOLF_POSITION_X, args.WOLF_POSITION_Y, args.DEPTH, args.WOLF_RANDOM, args.SHEEP_RANDOM)
