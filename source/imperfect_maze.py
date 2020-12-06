#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Implementation of 2D imperfect maze generation algorithms.
    Algorithms:
    - Serpentine algorithm
    - Small rooms algorithm
    - Spiral algorithm
"""

from random import randrange
from typing import List


def serpentine(y_max: int, x_max: int) -> List[List[bool]]:
    """
    Serpentine 2D imperfect maze generation algorithm
    :param y_max: height
    :param x_max: width
    :return: 2D imperfect maze grid
    """
    assert y_max % 2 and x_max % 2 and y_max >= 3 and x_max >= 3
    grid = [[True for _ in range(x_max)] for _ in range(y_max)]
    if randrange(2):
        for row in range(1, y_max - 1):
            grid[row][randrange(1, x_max - 1)] = False
            for col in range(1, x_max - 1, 2):
                grid[row][col] = False
        for col in range(2, x_max - 1, 4):
            grid[1][col] = False
        for col in range(4, x_max - 1, 4):
            grid[y_max - 2][col] = False
    else:
        for row in range(1, y_max - 1, 2):
            for col in range(1, x_max - 1):
                grid[row][col] = False
        for row in range(2, y_max - 1, 4):
            grid[row][1] = False
            grid[row][randrange(2, x_max - 1)] = False
        for row in range(4, y_max - 1, 4):
            grid[row][x_max - 2] = False
            grid[row][randrange(1, x_max - 2)] = False
    return grid


def small_rooms(y_max: int, x_max: int) -> List[List[bool]]:
    """
    Small rooms 2D imperfect maze generation algorithm
    :param y_max: height
    :param x_max: width
    :return: 2D imperfect maze grid
    """
    assert y_max % 2 and x_max % 2 and y_max >= 3 and x_max >= 3
    grid = [[True for _ in range(x_max)] for _ in range(y_max)]
    for y in range(1, y_max - 1):
        if y % 2:
            for x in range(1, x_max - 3, 4):
                grid[y][x] = False
                grid[y][x + 1] = False
                grid[y][x + 2] = False
                if x < x_max - 4 and not randrange(3):
                    grid[y][x + 3] = False
        else:
            for x in range(2, x_max - 1, 4):
                grid[y][x] = False
    y_mid = y_max // 2
    for x in range(1, x_max - 1):
        grid[y_mid][x] = False
    return grid


def spiral(y_max: int, x_max: int) -> List[List[bool]]:
    """
    Spiral 2D imperfect maze generation algorithm
    :param y_max: height
    :param x_max: width
    :return: 2D imperfect maze grid
    """
    assert y_max % 2 and x_max % 2 and y_max >= 3 and x_max >= 3
    grid = [[True for _ in range(x_max)] for _ in range(y_max)]
    directions = [(-2, 0), (0, 2), (2, 0), (0, -2)]
    if randrange(2):
        directions.reverse()
    current = (1, 1)
    grid[1][1] = False
    next_dir = 0
    while True:
        y, x = current
        new_y, new_x = (y + directions[next_dir][0], x + directions[next_dir][1])
        neighbors = ((y + dy, x + dx) for dy, dx in directions)
        neighbors = [(y, x) for y, x in neighbors if 0 < y < y_max and 0 < x < x_max if grid[y][x]]
        if (new_y, new_x) in neighbors:
            grid[(y + new_y) // 2][(x + new_x) // 2] = False
            grid[new_y][new_x] = False
            current = (new_y, new_x)
        elif not neighbors:
            break
        else:
            next_dir = (next_dir + 1) % 4
    for i in range(max(y_max, x_max)):
        grid[randrange(1, y_max - 1)][randrange(1, x_max - 1)] = False
    return grid


def main():
    from timeit import timeit

    def print_maze(maze):
        print(*[''.join('█' if col else ' ' for col in row) for row in maze], sep='\n')

    def get_input(string, begin, end):
        string += f" ({begin}-{end}):"
        input_result = input(string)
        while not (input_result.isdecimal() and begin <= int(input_result) <= end):
            input_result = input(string)
        return int(input_result)

    functions = [serpentine, small_rooms, spiral]
    n_functions = ['Serpentine algorithm', 'Small rooms algorithm', 'Spiral algorithm']
    time_functions = [0 for _ in n_functions]
    print('== Perfect maze ===')
    width = (get_input('Enter the width of the maze (odd number)', 5, 100000) // 2) * 2 + 1
    height = (get_input('Enter the height of the maze (odd number)', 5, 100000) // 2) * 2 + 1
    for n, func in zip(n_functions, functions):
        print(n)
        print_maze(func(height, width))
        input('next >>')
    print('\n', '=== Time test ===', 'Tests: 15', 'Sizes: 11-41', sep='\n')
    for i in range(15):
        y, x = (randrange(10, 40) // 2) * 2 + 1, (randrange(10, 40) // 2) * 2 + 1
        for j, func in enumerate(functions):
            name = func.__name__
            time_functions[j] += timeit(f"{name}({y}, {x})", f"from __main__ import {name}", number=15)
    for time, n in sorted(zip(time_functions, n_functions)):
        print(n + ': ' + str(time))
    input()


if __name__ == '__main__':
    main()

