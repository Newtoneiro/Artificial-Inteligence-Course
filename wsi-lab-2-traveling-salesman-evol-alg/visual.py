import pygame
import math
import random
from random import randint, sample, choice
import sys

GREEN = (50, 240, 50)
WIDTH, HEIGHT = 800, 800

pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Visualization")


class City:
    def __init__(self, WIN, x, y):
        self._win = WIN
        self.center = (x, y)
    
    def x(self):
        return self.center[0]
    
    def y(self):
        return self.center[1]
    
    def draw(self):
        pygame.draw.circle(self._win, GREEN, self.center, 3)
    
    def connect(self, city):
        pygame.draw.line(self._win, GREEN, self.center, city.center)


def Scatter_homogeneous(WIN, n:int, WIDTH:int, HEIGHT:int) -> list:
    max_rows = math.floor(math.sqrt(n))
    tested_rows = 1
    act_rows = 1
    while (n / tested_rows >= max_rows):
        if n % tested_rows == 0:
            act_rows = tested_rows
        tested_rows += 1
    act_cols = n / act_rows
    
    output = []
    W_jump = WIDTH // (int(act_cols) + 1)
    H_jump = HEIGHT // (int(act_rows) + 1)
    for row in range(0, int(act_rows)):
        for col in range(0, int(act_cols)):
            output.append(City(WIN, W_jump*(1 + col), H_jump*(1 + row)))
   
    return output


def Scatter_groups(WIN, n:int, WIDTH:int, HEIGHT:int) -> list:
    output = []
    while n > 0:
        members = randint(1, n)
        orientation_point = (randint(0, WIDTH), randint(0, HEIGHT))
        for _ in range(0, members):
            current_point = (0, 0)
            while current_point[0] <= 10 or current_point[0] >= WIDTH - 10 or current_point[1] <= 10 or current_point[1] >= HEIGHT - 10:
                current_point = (orientation_point[0] + randint(-70, 70), orientation_point[1] + randint(-70, 70))
            output.append(City(WIN, current_point[0], current_point[1]))
        n -= members
    
    return output


def Scatter_random(WIN, n:int, WIDTH:int, HEIGHT:int) -> list:
    output = []
    for _ in range(0, n):
        output.append(City(WIN, randint(10, WIDTH), randint(10, HEIGHT - 10)))
    return output


def Scatter(WIN, n:int, WIDTH:int, HEIGHT:int, type:int, seed:int = 0) -> list:
    if not seed:
        seed = random.randrange(sys.maxsize)
    random.seed(seed)
    print(f"The seed is : {seed}")
    
    if type == 0:
        return Scatter_homogeneous(WIN, n, WIDTH, HEIGHT)
    elif type == 1:
        return Scatter_groups(WIN, n, WIDTH, HEIGHT)
    elif type == 2:
        return Scatter_random(WIN, n, WIDTH, HEIGHT)
    else:
        return []


def CreateBeginPopulation(points:list, count:int) -> list:
    population = []
    for _ in range(0, count):
        population.append(sample(points, len(points)))
    return population


def TotalDistance(subject:list) -> float:
    distance = 0
    for i in range(1, len(subject)):
        distance += math.sqrt((subject[i].x() - subject[i-1].x() )**2 + (subject[i].y() - subject[i-1].y() )**2)
    return distance


def TournamentSelection(Population:list, PopulationCount:int):
    outputPopulation = []
    for _ in range(0, PopulationCount):
        a = choice(Population)
        b = choice(Population)
        outputPopulation.append(min([a, b], key=TotalDistance))
    return outputPopulation


def Mutate(Population:list, MutationProb:float) -> list:
    for i in range(0, len(Population)):
        if random.uniform(0, 1) < MutationProb:
            a = randint(0, len(Population[i]) - 1)
            b = randint(0, len(Population[i]) - 1)
            Population[i][a], Population[i][b] = Population[i][b], Population[i][a]
    return Population


def DrawConnections(pointList:list):
    global WIN
    for i in range(1, len(pointList)):
        pygame.draw.line(WIN, (255, 0, 0), pointList[i - 1].center, pointList[i].center)


def DrawNewBest(subject:list, points:list):
    global WIN
    WIN.fill((0, 0, 0))
    for point in points:
        point.draw()
    DrawConnections(subject)
    pygame.display.update()


def EvolutionAlghoritm(Population:list, PopulationCount:int, maxT:int, MutationProb:float, points:list) -> list:
    t = 0
    current_best = [City(city._win, city.x(), city.y()) for city in min(Population, key=TotalDistance)]
    
    print("=== Best in Population0 ====")
    print(TotalDistance(current_best))
    print("=========")
    DrawNewBest(current_best, points)
    
    while t < maxT:
        Population = TournamentSelection(Population, PopulationCount)
        Population = Mutate(Population, MutationProb)
        temp_best = min(Population, key=TotalDistance)
        
        if (TotalDistance(temp_best) < TotalDistance(current_best)):
            DrawNewBest(temp_best, points)
            current_best = [City(city._win, city.x(), city.y()) for city in temp_best]
        t += 1
    
    print("=== Best One Found ===")
    print(TotalDistance(current_best))
    print("=========")
    return current_best


def main():
    global WIN
    run = True
    points = Scatter(WIN, 30, WIDTH, HEIGHT, 2)
    population = CreateBeginPopulation(points, 30)
    EvolutionAlghoritm(population, 30, 5000, 0.3, points)
    for point in points:
        point.draw()
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()