from mpl_toolkits.mplot3d import art3d
from matplotlib import patches
import matplotlib.pyplot as plt
import numpy as np
import math
from random import uniform
import argparse


def function_z(x: float, y: float) -> float:
    return x**4 + 2*x*x*y - 21 * x**2 + 2 * x * y * y - 14 * x + y**4 - 13 * y * y - 22 * y + 170


def dx(x: float, y: float) -> float:
    return 4 * x * (x*x + y - 11) + 2 * (x + y*y - 7)


def dy(x: float, y: float) -> float:
    return 2 * (x * x + y - 11) + 4 * y * (x + y*y - 7)


def calculateGradient(x: float, y: float) -> tuple:
    return (dx(x, y), dy(x, y))


def mark3D(x:float, y:float, ax, size:float, color) -> None:
    plot = patches.Circle(
            (x, y),
            size,
            edgecolor=color,
            facecolor=color
        )
    ax.add_patch(plot)
    art3d.pathpatch_2d_to_3d(plot, function_z(x, y), zdir='z')


def main(B, iterations, TwoD):
    my_cmap = plt.get_cmap('hot')

    x_values = np.linspace(-5, 5, 20)
    y_values = np.linspace(-5, 5, 20)

    X, Y = np.meshgrid(x_values, y_values)
    Z = function_z(X, Y)

    xarr = []
    yarr = []
    
    x = uniform(-5, 5)
    y = uniform(-5, 5)
    xarr.append(x)
    yarr.append(y)

    Epsilon = 10e-8
    
    i = 0
    run = True

    while run and i < iterations:
        dx, dy = calculateGradient(x, y)
        x -= B * dx
        y -= B * dy
        xarr.append(x)
        yarr.append(y)
        i += 1
        if math.sqrt((xarr[i-1] - x)**2 + (yarr[i-1] - y)**2) < Epsilon:
            run = False
    print(f"X: {xarr[-1]} Y: {yarr[-1]}")
    # Create 3d plot
    if not TwoD:
        ax = plt.axes(projection='3d')
        ax.set_title("z = (x*x+y-11)^2 + (x+y*y-7)^2")
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')

        ax.plot_surface(X, Y, Z, cmap=my_cmap, alpha=0.8)

        mark3D(xarr[0], yarr[0], ax, 0.1, 'white')

        for x, y in zip(xarr, yarr):
            mark3D(x, y, ax, 0.05, 'black')
        
        mark3D(xarr[-1], yarr[-1], ax, 0.1, 'red')
    
    #Create 2d colormap
    else:
        X_list = np.arange(-5, 5, 0.1)
        Y_list = np.arange(-5, 5, 0.1)
        Z_list = []
        for x in X_list:
            row = []
            for y in Y_list:
                row.append(function_z(x, y))
            Z_list.append(row)

        pc = plt.pcolormesh(X_list, Y_list, Z_list, cmap=my_cmap)
        plt.contour(X_list, Y_list, Z_list, 15, colors='black')

        plt.scatter(xarr, yarr, color='white')
        plt.scatter(xarr[0], yarr[0], color='black', s=1e2)
        plt.scatter(xarr[-1], yarr[-1], color='red', s=1e2)
        plt.title(f"Beta: {B}  Iterations: {i}")

        cbar = plt.colorbar(pc)
        cbar.set_label("z = f(x, y)", rotation=0, labelpad = 30)

    # Creating plot
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-B', '--Beta', type=float, required=True, help='Beta argument (Step length)')
    parser.add_argument('-I', '--Iterations', type=int, required=True, help='Max steps')
    parser.add_argument('-D', '--TwoD', action='store_true', help='2D or 3D plot (true = 2D) ')
    args = parser.parse_args()
    main(args.Beta, args.Iterations, args.TwoD)
