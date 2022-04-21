import random
import numpy as np

class QLearning:
    def __init__(self, board, episodes, discount_factor, learning_rate, epsilon) -> None:
        self._board = board
        self._episodes = episodes
        self._epsilon = epsilon
        self._discount_factor = discount_factor
        self._learning_rate = learning_rate

        self._q_values = np.zeros((len(self._board), len(self._board), 4))

    def getStartingLocation(self):
        pos = (random.randint(0, len(self._board) - 1), random.randint(0, len(self._board) - 1))
        while self._board[pos[0]][pos[1]] != -1:
            pos = (random.randint(0, len(self._board) - 1), random.randint(0, len(self._board) - 1))
        return pos

    def isTerminalState(self, row, col):
        if self._board[row][col] != -1:
            return True
        return False

    def getNextAction(self, row, col, learning=True):
        if learning:
            if random.uniform(0, 1) < self._epsilon:
                return np.argmax(self._q_values[row][col])
            else:
                return np.random.randint(0, 3)
        else:
            return np.argmax(self._q_values[row][col])
    
    def getNextLocation(self, row, col, action):
        if action == 0: # go up
            if row > 0:
                return (0, (row - 1, col))
        if action == 1: # go right
            if col < len(self._board) - 1:
                return (0, (row, col + 1))
        if action == 2: # go down
            if row < len(self._board) - 1:
                return (0, (row + 1, col))
        if action == 3: # go left
            if col > 0:
                return (0, (row, col - 1))
        return (-100, [row, col]) # If hit the border

    def train(self):
        for ep in range(self._episodes):
            row, col = self.getStartingLocation()
            while not self.isTerminalState(row, col):
                action = self.getNextAction(row, col)

                prev_row, prev_col = row, col
                bonus_penalty, move = self.getNextLocation(row, col, action)
                row, col = move[0], move[1]

                reward = self._board[row][col] + bonus_penalty
                old_q_val = self._q_values[prev_row, prev_col, action]
                temporal_difference = reward + (self._discount_factor * np.max(self._q_values[row, col])) - old_q_val

                new_q_val = old_q_val + (self._learning_rate * temporal_difference)
                self._q_values[prev_row, prev_col, action] = new_q_val
            print(f"{ep} / {self._episodes}")
            
        print("Learning complete.")
    
    def getShortestPath(self, row, col):
        # if invalid starting pos
        path = []
        if self.isTerminalState(row, col):
            return path
        else:
            i = 0
            while not self.isTerminalState(row, col) and i < len(self._board)**2:
                next_action = self.getNextAction(row, col, False)
                _, move = self.getNextLocation(row, col, next_action)
                row, col = move
                path.append([row, col])
                i += 1
        return path


