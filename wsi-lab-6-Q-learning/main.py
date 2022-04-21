import pygame
import random
import sys

from Q_Learning import QLearning

WIDTH, HEIGHT = 800, 800

BLACK = (0, 0, 0)
GREYISH = (200, 200, 200)
WHITE = (255, 255 ,255)
RED = (255, 50, 50)
YELLOW = (224, 232, 70)

pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Q-Uber")

class Board:
    def __init__(self, size, WIN, width, height, start, goal, penalties):
        self._size = size
        self._win = WIN

        self._start = start
        self._goal = goal
        self._penalties = penalties
        
        self._width = width
        self._height = height
        self._outline = 2
        self._square_size = width / size

        self.initMaze()
    
    def initBoard(self):
        self._board = [[0 for i in range(self._size)] for j in range(self._size)]
        self._board[self._goal[0]][self._goal[1]] = 100
    
    def initMaze(self):
        check = False
        while not check:
            
            self.initBoard()
            
            for _ in range(self._penalties):
                position = [random.randint(0, self._size - 1) for _ in range(0, 2)]
                while self._board[position[0]][position[1]] != 0:
                    position = [random.randint(0, self._size - 1) for _ in range(0, 2)]
                self._board[position[0]][position[1]] = -100
            
            check = self.checkMaze()
            if not check:
                print("Maze generated incorectly, trying again.")
    
    def checkMaze(self, start_pos = None):
        if not start_pos:
            start_pos = self._start
        check = False
        stack = [start_pos]
        while len(stack) > 0:
            cur_pos = stack.pop()
            moves = self.findAdjacent(cur_pos)
            for move in moves:
                stack.append(move)
            
            if cur_pos[0] == self._goal[0] and cur_pos[1] == self._goal[1]:
                check = True
            else:
                self._board[cur_pos[0]][cur_pos[1]] = -1
        
        return check
    
    def findAdjacent(self, pos, forRandomCar = False):
        row, col = pos
        available = []
        if row < self._size - 1:
            if self._board[row+1][col] >= 0 or forRandomCar:
                available.append((row+1, col))
        if row > 0:
            if self._board[row-1][col] >= 0 or forRandomCar:
                available.append((row-1, col))
        if col < self._size - 1:
            if self._board[row][col+1] >= 0 or forRandomCar:
                available.append((row, col+1))
        if col > 0:
            if self._board[row][col-1] >= 0 or forRandomCar:
                available.append((row, col-1))      

        return available
    
    def getRandomCarPath(self, row, col):
        cur_pos = (row, col)
        path = [cur_pos]
        while not (cur_pos[0] == self._goal[0] and cur_pos[1] == self._goal[1]):
            moves = self.findAdjacent(cur_pos, True)
            cur_pos = random.choice(moves)
            path.append(cur_pos)
            if len(path) > 10000:
                return path
        return path

    def draw(self, start_pos = None):
        if not start_pos:
            start_pos = self._start
        self._win.fill(BLACK)
        pygame.draw.rect(self._win, GREYISH, (self._outline, self._outline, self._width - self._outline, self._height - self._outline))
        for row in range(0, self._size):
            for col in range(row % 2, self._size, 2):
                pygame.draw.rect(self._win, BLACK, (col * self._square_size, row * self._square_size, self._square_size + self._outline, self._square_size + self._outline))
                pygame.draw.rect(self._win, WHITE, (col * self._square_size + self._outline, row * self._square_size + self._outline, (self._square_size - self._outline), (self._square_size - self._outline)))

        for row in range(self._size):
            for col in range(self._size):
                if self._board[row][col] in [-100, 100]:
                    if self._board[row][col] == -100:
                        color = BLACK
                    elif self._board[row][col] == 100:
                        color = YELLOW
                    pygame.draw.rect(self._win, color, (col * self._square_size + self._outline, row * self._square_size + self._outline, (self._square_size - self._outline), (self._square_size - self._outline)))
                if row == start_pos[0] and col == start_pos[1]:
                    pygame.draw.rect(self._win, RED, (col * self._square_size + self._outline, row * self._square_size + self._outline, (self._square_size - self._outline), (self._square_size - self._outline)))
        pygame.display.update()
    
    def drawPath(self, start_pos, path):
        self.draw(start_pos)
        for move in path[:-1]:
            row = move[0]
            col = move[1]
            pygame.draw.rect(self._win, (100, 50, 255), (col * self._square_size + self._outline, row * self._square_size + self._outline, (self._square_size - self._outline), (self._square_size - self._outline)))
        pygame.display.update()
    
    def getSquare(self, x, y):
        col = int(x // self._square_size)
        row = int(y // self._square_size)
        return (row, col)

def differentiate(q, board, n):
    r_lengths = []
    q_lengths = []
    start_pos = [0, 0]
    for _ in range(n):
        start_pos[0] = random.randint(0, len(board._board) - 1)
        start_pos[1] = random.randint(0, len(board._board) - 1)
        
        random_path = board.getRandomCarPath(start_pos[0], start_pos[1])
        r_lengths.append(len(random_path))
        q_path = q.getShortestPath(start_pos[0], start_pos[1])
        if len(q_path) != 0:
            q_lengths.append(len(q_path))
    avg_r = sum(r_lengths) / len(r_lengths)
    avg_q = sum(q_lengths) / len(q_lengths)
    return avg_r, avg_q


def main():
    run = True

    seed = 0
    if not seed:
        seed = random.randrange(sys.maxsize)
    random.seed(seed)
    print(f"The seed is : {seed}")

    board = Board(25, WIN, WIDTH, HEIGHT, (0, 0), (24, 24), 250)
    board.draw()
    q = QLearning(board._board, 10000, 0.9, 0.5, 0.99)
    q.train()

    print(differentiate(q, board, 500))

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row, col = board.getSquare(x, y)
                path = q.getShortestPath(row, col)
                board.drawPath((row, col), path)
    pygame.quit()

if __name__ == "__main__":
    main()