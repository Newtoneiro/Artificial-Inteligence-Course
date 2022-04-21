from constants import *
from random import choice
import pygame
from sys import maxsize

class Checker:
    """
    Class representing either a Sheep or the Wolf.
    It holds the information about the checker's role and its position
    """
    def __init__(self, win: pygame.display, role: int, row: int, col: int, sqsz: int, outline: int):
        self._win = win
        self._role = role
        self._row = row
        self._col = col
        self._square_size = sqsz
        self._outline = outline

    def role(self) -> int:
        return self._role

    def row(self) -> int:
        return self._row

    def col(self) -> int:
        return self._col

    def move(self, row: int, col: int) -> None:
        self._row = row
        self._col = col

    def draw(self) -> None:
        """
        Draw the checker
        """
        colour = BLACK          #if Woolf
        if self._role == 0:     #if Sheep
            colour = WHITE
        pygame.draw.circle(self._win, BLACK, (self._col * self._square_size + self._square_size // 2, self._row * self._square_size + self._square_size //2), 0.3 * self._square_size)
        pygame.draw.circle(self._win, colour, (self._col * self._square_size + self._square_size // 2, self._row * self._square_size + self._square_size //2), 0.3 * self._square_size - self._outline)


class Board:
    """
    Main class of the program, holds the information
    about it's state, current checkers placement,
    is responsible for updating the game and
    visualizing it.
    """
    def __init__(self, WIN: pygame.display, width: int, height: int, size: int, wolf_x: int, wolf_y: int, depth: int, wolf_rand: bool, sheep_rand: bool):
        self._turn = 1
        self._width = width
        self._height = height
        self._size = size
        self._win = WIN
        self._square_size = width / size
        self._outline = 2
        self._minmax_depth = depth
        self._wolf_random = wolf_rand
        self._sheep_random = sheep_rand
        self.initBoard(wolf_x, wolf_y)

    def switchTurns(self):
        self._turn = (self._turn + 1) % 2

    def availableMoves(self, checker: Checker, position: list) -> list:
        """
        Return available moves for checker in current position
        """
        if checker is None:
            return []
        available_moves = []

        direction = 1               #if Woolf
        if checker._role == 0:      #if Sheep
            direction = -1

        if (checker.row() - direction) >= 0 and (checker.row() - direction) < self._size:
            if (checker.col() - 1) >= 0 and (checker.col() - 1) < self._size:
                if position[checker.row() - direction][checker.col() - 1] is None:
                    available_moves.append((checker.row() - direction, checker.col() - 1))

            if (checker.col() + 1) >= 0 and (checker.col() + 1) < self._size:
                if position[checker.row() - direction][checker.col() + 1] is None:
                    available_moves.append((checker.row() - direction, checker.col() + 1))

        if checker._role == 1: # Wolf can move backwards
            if (checker.row() + direction) >= 0 and (checker.row() + direction) < self._size:
                if (checker.col() - 1) >= 0 and (checker.col() - 1) < self._size:
                    if position[checker.row() + direction][checker.col() - 1] is None:
                        available_moves.append((checker.row() + direction, checker.col() - 1))
                if (checker.col() + 1) >= 0 and (checker.col() + 1) < self._size:
                    if position[checker.row() + direction][checker.col() + 1] is None:
                        available_moves.append((checker.row() + direction, checker.col() + 1))

        return available_moves

    def moveChecker(self, checker: Checker, move: tuple, position: list) -> None:
        """
        Move checker, update both the position and checker's coordinates
        """
        position[checker.row()][checker.col()], position[move[0]][move[1]] = position[move[0]][move[1]], position[checker.row()][checker.col()]
        checker.move(move[0], move[1])

    def initBoard(self, x: int, y: int) -> None:
        """
        Initialize The Board, fill it with created Checkers and empty spaces. Put
        wolf's piece in (x, y) place if possible.
        """
        if (not (x > 0 and x < self._size - 1)) or (y + ( x % 2 )) % 2 == 0:
            print("==================================================================")
            print("Incorrect wolf's starting position, initializing with default one.")
            print("==================================================================")
            x = self._size - 1
            y = self._size % 2

        self._board = []
        for row in range(self._size):
            self._board.append([])
            for col in range(self._size):
                if row == 0 and col % 2 == 1:
                    self._board[row].append(Checker(self._win, 0, row, col, self._square_size, self._outline))
                else:
                    self._board[row].append(None)
        
        # initialize wolf
        self._board[x][y] = Checker(self._win, 1, x, y, self._square_size, self._outline)

    def draw(self) -> None:
        # Draw the board
        self._win.fill(BLACK)
        pygame.draw.rect(self._win, REDDISH, (self._outline, self._outline, self._width - self._outline, self._height - self._outline))
        for row in range(0, self._size):
            for col in range(row % 2, self._size, 2):
                pygame.draw.rect(self._win, BLACK, (col * self._square_size, row * self._square_size, self._square_size + self._outline, self._square_size + self._outline))
                pygame.draw.rect(self._win, WHITE, (col * self._square_size + self._outline, row * self._square_size + self._outline, (self._square_size - self._outline), (self._square_size - self._outline)))
        # Draw the checkers
        for row in range(self._size):
            for col in range(self._size):
                if self._board[row][col] is not None:
                    self._board[row][col].draw()

        pygame.display.update()

    def endGame(self) -> None:
        """
        Endgame sequence
        """
        self.switchTurns()
        winner = ' Wilk'
        if self._turn == 0:
            winner = 'ją Owce'
        print(f"====== Wygrywa{winner} =======")

    def compareMoves(self, move: tuple) -> int:
        """
        Used to return estimated value of the move according to current game state.
        """
        child_pos = []
        for i, row in enumerate(self._board):
            child_pos.append([])
            for checker in row:
                if checker is None:
                    child_pos[i].append(None)
                else:
                    child_pos[i].append(Checker(checker._win, checker.role(), checker.row(), checker.col(), checker._square_size, checker._outline))
        self.moveChecker(child_pos[move[0].row()][move[0].col()], move[1], child_pos)

        return self.minmax(child_pos, self._minmax_depth, (self._turn + 1) % 2)

    def update(self) -> bool:
        sheep_moves, wolf_moves = self.getSheepAndWolfMoves(self._board)
        moves = wolf_moves
        if self._turn == 0:
            moves = sheep_moves

        if len(moves) > 0:
            if self._turn == 0:
                if not self._sheep_random:
                    move_tuple = min(moves, key=self.compareMoves)
                else:
                    move_tuple = choice(moves)
            else:
                if not self._wolf_random:
                    move_tuple = max(moves, key=self.compareMoves)
                else:
                    move_tuple = choice(moves)

            chckr = move_tuple[0]
            move = move_tuple[1]

            self.moveChecker(chckr, move, self._board)
            self.switchTurns()
            self.draw()
            if chckr._role == 1 and move[0] == 0:
                self.endGame()
                return True
        else:
            self.endGame()
            return True
        return False

    def getSheepAndWolfMoves(self, position: list) -> tuple:
        """
        Return all the possible moves for wolf and the sheeps in given position
        """
        sheep_moves = []
        wolf_moves = []
        for row in range(self._size):
            for col in range(self._size):
                checker = position[row][col]
                if checker is not None:
                    if checker.role() == 1:
                        for move in self.availableMoves(checker, position):
                            wolf_moves.append((checker, move))
                    elif checker.role() == 0:
                        for move in self.availableMoves(checker, position):
                            sheep_moves.append((checker, move))
        return sheep_moves, wolf_moves

    def determineEndGame(self, position: list) -> bool:
        """
        Determine if the game is over
        """
        for row in range(self._size):
            for col in range(self._size):
                checker = position[row][col]
                if checker is not None:
                    if checker.role() == 1 and checker.row() == 0:
                        return True
        sheep_moves, wolf_moves = self.getSheepAndWolfMoves(position)
        if len(sheep_moves) == 0 or len(wolf_moves) == 0:
            return True
        return False

    def evaluate(self, position: list) -> int:
        """
        Return the estimated value of current position.
        (Higher score favours the wolf player)
        """
        score = 0
        sheep_moves, wolf_moves = self.getSheepAndWolfMoves(position)
        for component in position[0]:
            if component is not None:
                if component._role == 1:
                    score += 1000
        if len(wolf_moves) > 0:
            score += 10*(self._size - wolf_moves[0][0].row())
            for _ in wolf_moves:
                score += 5
        return score


    def minmax(self, position: list, depth: int, wolf_turn: bool) -> int:
        """
        The minmax alghoritm
        """
        if depth == 0 or self.determineEndGame(position):
            return self.evaluate(position)

        sh_mv, wf_mv = self.getSheepAndWolfMoves(position)

        if wolf_turn:
            maxEval = -maxsize
            for mv in wf_mv:
                child_pos = []
                for i, row in enumerate(position):
                    child_pos.append([])
                    for checker in row:
                        if checker is None:
                            child_pos[i].append(None)
                        else:
                            child_pos[i].append(Checker(checker._win, checker.role(), checker.row(), checker.col(), checker._square_size, checker._outline))

                self.moveChecker(child_pos[mv[0].row()][mv[0].col()], mv[1], child_pos)
                eval = self.minmax(child_pos, depth-1, False)
                maxEval = max(eval, maxEval)
            return maxEval

        else:
            minEval = maxsize
            for mv in sh_mv:
                child_pos = []
                for i, row in enumerate(position):
                    child_pos.append([])
                    for checker in row:
                        if checker is None:
                            child_pos[i].append(None)
                        else:
                            child_pos[i].append(Checker(checker._win, checker.role(), checker.row(), checker.col(), checker._square_size, checker._outline))

                self.moveChecker(child_pos[mv[0].row()][mv[0].col()], mv[1], child_pos)
                eval = self.minmax(child_pos, depth-1, True)
                minEval = min(eval, minEval)
            return minEval
