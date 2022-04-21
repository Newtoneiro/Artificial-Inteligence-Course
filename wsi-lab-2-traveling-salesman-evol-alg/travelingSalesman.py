import pygame
import math
import random
from random import randint, sample, choice
import sys
import argparse
from matplotlib import pyplot as plt

# Constants
GREEN = (50, 240, 50)
WIDTH, HEIGHT = 800, 800

#Pygame stuff
pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Visualization")


# Visual
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


def DrawConnections(pointList:list):
    global WIN
    for i in range(0, len(pointList)):
        pygame.draw.line(WIN, (255, 0, 0), pointList[i - 1].center, pointList[i].center)


def DrawNewBest(subject:list, points:list):
    global WIN
    WIN.fill((0, 0, 0))
    for point in points:
        point.draw()
    DrawConnections(subject)
    pygame.display.update()


# -- Scatter cities functions --
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

# Helpers for actual alghoritm
def CreateBeginPopulation(points:list, count:int) -> list:
    population = []
    for _ in range(0, count):
        population.append(sample(points, len(points)))
    return population


def TotalDistance(subject:list) -> float:
    distance = 0
    for i in range(0, len(subject)):
        distance += math.sqrt((subject[i].x() - subject[i-1].x() )**2 + (subject[i].y() - subject[i-1].y() )**2)
    return distance


def TournamentSelection(Population:list, PopulationCount:int):
    outputPopulation = []
    for _ in range(0, PopulationCount):
        a = choice(Population)
        b = choice(Population)
        outputPopulation.append([City(city._win, city.x(), city.y()) for city in min([a, b], key=TotalDistance)]) #Deep Copy
    return outputPopulation


def Mutate(Population:list, PopMProb:float) -> list:
    for i in range(0, len(Population)):
        if random.uniform(0, 1) < PopMProb:
            GeneIndex = randint(0, len(Population[i]) - 1)
            SwapGeneIndex = randint(0, len(Population[i]) - 1)
            cityA = Population[i][SwapGeneIndex]
            cityB = Population[i][GeneIndex]
            Population[i][GeneIndex], Population[i][SwapGeneIndex] = City(cityA._win, cityA.x(), cityA.y()), City(cityB._win, cityB.x(), cityB.y()) #Deep Copy
    return Population

# Actual alghoritm
def EvolutionAlghoritm(Population:list, PopulationCount:int, maxT:int, PopMProb:float, points:list) -> list:
    t = 0
    current_best = [City(city._win, city.x(), city.y()) for city in min(Population, key=TotalDistance)]

    #plots
    x_arr = []
    y_arr = []
    
    print("=== Best in Population0 ====")
    print(TotalDistance(current_best))
    print("=========")
    DrawNewBest(current_best, points)
    
    while t < maxT:
        Population = TournamentSelection(Population, PopulationCount)
        Population = Mutate(Population, PopMProb)
        
        temp_best = min(Population, key=TotalDistance)
        
        if (TotalDistance(temp_best) < TotalDistance(current_best)):
            DrawNewBest(temp_best, points)
            current_best = [City(city._win, city.x(), city.y()) for city in temp_best]
        
        #plots
        x_arr.append(t)
        y_arr.append(TotalDistance(temp_best))
        t += 1
        print(t)
    
    print("=== Best One Found ===")
    print(TotalDistance(current_best))
    print("=========")

    #plot
    plt.plot(x_arr, y_arr, 'bo', alpha=0.3)
    plt.title("Best Distance to Generation ratio")
    plt.xlabel("Generation")
    plt.ylabel("Total Distance")
    plt.show()

    return current_best


def main(NoC: int, SM: int, PopC: int, Iter: int, PopMProb: float, Seed :int = 0):
    global WIN
    run = True

    if SM not in (0, 1, 2):
        SM = 2
    
    points = Scatter(WIN, NoC, WIDTH, HEIGHT, SM, Seed)
    population = CreateBeginPopulation(points, PopC)
    
    EvolutionAlghoritm(population, PopC, Iter, PopMProb, points)
    
    for point in points:
        point.draw()
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-N', '--NumberOfCities', type=int, required=True, help='Number of points in graph (Cities)')
    parser.add_argument('-SM', '--ScatterMode', type=int, required=True, help='Type of scatter used : 0 - homogeneous, 1 - Groups, 2 - Random')
    parser.add_argument('-PopCount', '--PopulationCount', type=int, required=True, help='Number of specimens in populations')
    parser.add_argument('-Iter', '--Iterations', type=int, required=True, help='Max No. of Iterations in alghoritm')
    parser.add_argument('-PMProb', '--PopulationMutationProb', type=float, required=True, help='Probability of specimens mutation')
    parser.add_argument('-Seed', '--Seed', type=float, required=False, help='The Seed for random() functions')
    args = parser.parse_args()
    main(args.NumberOfCities, args.ScatterMode, args.PopulationCount, args.Iterations, args.PopulationMutationProb, args.Seed)