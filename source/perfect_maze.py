#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Implementation of 2D perfect maze generation algorithms.
    Algorithms:
    - Aldous-Broder algorithm (unbiased maze)
    - Wilson's algorithm (unbiased maze)
    - Backtracking (depth-first search, iterative version)
    - Binary tree algorithm
    - Division algorithm
    - Eller's algorithm
    - Growing tree algorithm
    - Kruskal's algorithm
    - Prim's algorithm
    - Prim's algorithm (modified)
    - Sidewinder algorithm
"""

from random import choice, random, randrange, sample, shuffle
from typing import List


def aldous_broder(y_max: int, x_max: int) -> List[List[bool]]:
    """
    Aldous-Broder 2D perfect maze generation algorithm (unbiased maze)
    :param y_max: height
    :param x_max: width
    :return: 2D perfect maze grid
    """
    assert y_max % 2 and x_max % 2 and y_max >= 3 and x_max >= 3
    grid = [[True for _ in range(x_max)] for _ in range(y_max)]
    directions = ((2, 0), (-2, 0), (0, 2), (0, -2))
    (current_row, current_col) = (randrange(1, y_max, 2), randrange(1, x_max, 2))
    grid[current_row][current_col] = False
    num_visited = 1
    max_visited = ((y_max - 1) // 2 * (x_max - 1) // 2)
    while num_visited < max_visited:
        neighbors = [(current_row + dy, current_col + dx) for dy, dx in directions]
        valid_neighbors = [(y, x) for y, x in neighbors if 0 < y < y_max and 0 < x < x_max and grid[y][x]]
        if not valid_neighbors:
            free_neighbors = [(y, x) for y, x in neighbors if 0 < y < y_max and 0 < x < x_max and not grid[y][x]]
            (current_row, current_col) = choice(free_neighbors)
            continue
        shuffle(valid_neighbors)
        for new_row, new_col in valid_neighbors:
            if grid[new_row][new_col]:
                grid[new_row][new_col] = grid[(new_row + current_row) // 2][(new_col + current_col) // 2] = False
                (current_row, current_col) = (new_row, new_col)
                num_visited += 1
                break
    return grid


def wilson(y_max: int, x_max: int) -> List[List[bool]]:
    """
    Wilson's 2D perfect maze generation algorithm (unbiased maze)
    :param y_max: height
    :param x_max: width
    :return: 2D perfect maze grid
    """
    assert y_max % 2 and x_max % 2 and y_max >= 3 and x_max >= 3
    grid = [[True for _ in range(x_max)] for _ in range(y_max)]
    directions = ((2, 0), (-2, 0), (0, 2), (0, -2))
    free = {(y, x) for y in range(1, y_max, 2) for x in range(1, x_max, 2)}
    (y, x) = (2 * randrange(y_max // 2) + 1, 2 * randrange(x_max // 2) + 1)
    grid[y][x] = False
    free.remove((y, x))
    while free:
        y, x = key = sample(free, 1)[0]
        free.remove(key)
        path = [key]
        grid[y][x] = False
        neighbors = ((y + dy, x + dx) for dy, dx in directions)
        neighbors = [(y, x) for y, x in neighbors if 0 < y < y_max and 0 < x < x_max]
        y, x = key = choice(neighbors)
        while grid[y][x]:
            grid[y][x] = grid[(y + path[-1][0]) // 2][(x + path[-1][1]) // 2] = False
            neighbors = ((y + dy, x + dx) for dy, dx in directions)
            neighbors = [(y, x) for y, x in neighbors if 0 < y < y_max and 0 < x < x_max]
            neighbors.remove(path[-1])
            free.remove(key)
            path.append(key)
            y, x = key = choice(neighbors)
        if key in path:
            last_key = path.pop()
            free.add(last_key)
            grid[last_key[0]][last_key[1]] = True
            for key in reversed(path):
                free.add(key)
                grid[key[0]][key[1]] = grid[(last_key[0] + key[0]) // 2][(last_key[1] + key[1]) // 2] = True
                last_key = key
        else:
            grid[(y + path[-1][0]) // 2][(x + path[-1][1]) // 2] = False
    return grid


def backtracking(y_max: int, x_max: int) -> List[List[bool]]:
    """
    Iterative version of depth-first search 2D perfect maze generation algorithm
    :param y_max: height
    :param x_max: width
    :return: 2D perfect maze grid
    """
    grid = [[True for _ in range(x_max)] for _ in range(y_max)]
    directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
    stack = [(2 * randrange(y_max // 2) + 1, 2 * randrange(x_max // 2) + 1)]
    while stack:
        y, x = stack.pop()
        grid[y][x] = False
        neighbors = ((y + dy, x + dx) for dy, dx in directions)
        neighbors = [(y, x) for y, x in neighbors if 0 < y < y_max and 0 < x < x_max and grid[y][x]]
        if len(neighbors) > 1:
            stack.append((y, x))
        if neighbors:
            ny, nx = choice(neighbors)
            grid[(y + ny) // 2][(x + nx) // 2] = False
            stack.append((ny, nx))
    return grid


def binary_tree(y_max: int, x_max: int) -> List[List[bool]]:
    """
    Binary tree 2D perfect maze generation algorithm
    :param y_max: height
    :param x_max: width
    :return: 2D perfect maze grid
    """
    assert y_max % 2 and x_max % 2 and y_max >= 3 and x_max >= 3
    grid = [[True for _ in range(x_max)] for _ in range(y_max)]
    grid[1][1] = False
    for x in range(3, x_max, 2):
        grid[1][x] = grid[1][x - 1] = False
    for y in range(3, y_max, 2):
        grid[y][1] = grid[y - 1][1] = False
        for x in range(3, x_max, 2):
            if randrange(2):
                grid[y][x] = grid[y][x - 1] = False
            else:
                grid[y][x] = grid[y - 1][x] = False
    return grid


def division(y_max: int, x_max: int) -> List[List[bool]]:
    """
    Division 2D perfect maze generation algorithm
    :param y_max: height
    :param x_max: width
    :return: 2D perfect maze grid
    """
    assert y_max % 2 and x_max % 2 and y_max >= 3 and x_max >= 3
    HORIZONTAL, VERTICAL = 1, 0
    grid = [[False for _ in range(x_max)] for _ in range(y_max)]
    for i in range(len(grid[0])):
        grid[0][i] = grid[-1][i] = True
    for i in range(len(grid)):
        grid[i][0] = grid[i][-1] = True
    region_stack = [((1, 1), (y_max - 2, x_max - 2))]
    while region_stack:
        current_region = region_stack[-1]
        region_stack.pop()
        ((min_y, min_x), (max_y, max_x)) = current_region
        (height, width) = (max_y - min_y + 1, max_x - min_x + 1)
        if height <= 1 or width <= 1:
            continue
        if width < height:
            cut_direction = HORIZONTAL
        elif width > height:
            cut_direction = VERTICAL
        else:
            if width == 2:
                continue
            cut_direction = randrange(2)
        cut_length = (height, width)[(cut_direction + 1) % 2]
        if cut_length < 3:
            continue
        cut_pos = randrange(1, cut_length, 2)
        door_pos = randrange(0, (height, width)[cut_direction], 2)
        if cut_direction == VERTICAL:
            for row in range(min_y, max_y + 1):
                grid[row][min_x + cut_pos] = True
            grid[min_y + door_pos][min_x + cut_pos] = False
        else:
            for col in range(min_x, max_x + 1):
                grid[min_y + cut_pos][col] = True
            grid[min_y + cut_pos][min_x + door_pos] = False
        if cut_direction == VERTICAL:
            region_stack.append(((min_y, min_x), (max_y, min_x + cut_pos - 1)))
            region_stack.append(((min_y, min_x + cut_pos + 1), (max_y, max_x)))
        else:
            region_stack.append(((min_y, min_x), (min_y + cut_pos - 1, max_x)))
            region_stack.append(((min_y + cut_pos + 1, min_x), (max_y, max_x)))
    return grid


def eller(y_max: int, x_max: int) -> List[List[bool]]:
    """
    Eller's 2D perfect maze generation algorithm
    :param y_max: height
    :param x_max: width
    :return: 2D perfect maze grid
    """
    assert y_max % 2 and x_max % 2 and y_max >= 3 and x_max >= 3
    grid = [[True for _ in range(x_max)] for _ in range(y_max)]
    parent = {x: {x} for x in range(1, x_max, 2)}
    for y in range(1, y_max - 2, 2):
        grid[y][1] = False
        for x in range(3, x_max, 2):
            if x not in parent[x - 2] and randrange(2):
                parent[x].update(parent[x - 2])
                for key in list(parent[x - 2]):
                    parent[key] = parent[x]
                grid[y][x - 1] = grid[y][x] = False
            else:
                grid[y][x] = False
        for members in {frozenset(x) for x in parent.values()}:
            walls = [list(), list()]
            for x in members:
                walls[randrange(2)].append(x)
            if not walls[0]:
                walls.reverse()
            for x in walls[0]:
                grid[y + 1][x] = False
            for x in walls[1]:
                for key in parent:
                    parent[key].discard(x)
                parent[x] = {x}
    y = y_max - 2
    grid[y][1] = False
    for x in range(3, x_max, 2):
        if x not in parent[x - 2]:
            parent[x].update(parent[x - 2])
            for key in list(parent[x - 2]):
                parent[key] = parent[x]
            grid[y][x - 1] = grid[y][x] = False
        else:
            grid[y][x] = False
    return grid


def growing_tree(y_max: int, x_max: int, backtrack_chance: float = 0.5) -> List[List[bool]]:
    """
    Growing tree 2D perfect maze generation algorithm
    :param y_max: height
    :param x_max: width
    :param backtrack_chance: splits the logic to either use Recursive Backtracking (RB) or Prim's (random) to select
        the next cell to visit (default 1.0)
    :return: 2D perfect maze grid
    """
    assert y_max % 2 and x_max % 2 and y_max >= 3 and x_max >= 3
    grid = [[True for _ in range(x_max)] for _ in range(y_max)]
    directions = ((2, 0), (-2, 0), (0, 2), (0, -2))
    current_row, current_col = (randrange(1, y_max, 2), randrange(1, x_max, 2))
    grid[current_row][current_col] = False
    active = [(current_row, current_col)]
    while active:
        if random() < backtrack_chance:
            current_row, current_col = active[-1]
        else:
            current_row, current_col = choice(active)
        neighbors = ((current_row + dy, current_col + dx) for dy, dx in directions)
        neighbors = [(y, x) for y, x in neighbors if 0 < y < y_max and 0 < x < x_max and grid[y][x]]
        if not neighbors:
            active = [a for a in active if a != (current_row, current_col)]
            continue
        nn_row, nn_col = choice(neighbors)
        active += [(nn_row, nn_col)]
        grid[nn_row][nn_col] = False
        grid[(current_row + nn_row) // 2][(current_col + nn_col) // 2] = False
    return grid


def kruskal(y_max: int, x_max: int) -> List[List[bool]]:
    """
    Kruskal's 2D perfect maze generation algorithm
    :param y_max: height
    :param x_max: width
    :return: 2D perfect maze grid
    """
    assert y_max % 2 and x_max % 2 and y_max >= 3 and x_max >= 3
    grid = [[True for _ in range(x_max)] for _ in range(y_max)]
    parent = {(y, x): (y, x) for y in range(1, y_max, 2) for x in range(1, x_max, 2)}

    def find(x):
        temp = x[:]
        while parent[temp] != temp:
            temp = parent[temp]
        return temp

    walls = [(1, x) for x in range(2, x_max - 1, 2)]
    for y in range(2, y_max - 2, 2):
        walls.extend((y, x) for x in range(1, x_max, 2))
        y += 1
        walls.extend((y, x) for x in range(2, x_max - 1, 2))
    shuffle(walls)
    for y, x in walls:
        if y % 2:
            coord1 = (y, x + 1)
            coord2 = (y, x - 1)
        else:
            coord1 = (y + 1, x)
            coord2 = (y - 1, x)
        if find(coord1) != find(coord2):
            grid[y][x] = grid[coord1[0]][coord1[1]] = grid[coord2[0]][coord2[1]] = False
            parent[find(coord1)] = find(coord2)
    return grid


def prim(y_max: int, x_max: int) -> List[List[bool]]:
    """
    Prim's 2D perfect maze generation algorithm
    :param y_max: height
    :param x_max: width
    :return: 2D perfect maze grid
    """
    assert y_max % 2 and x_max % 2 and y_max >= 3 and x_max >= 3
    grid = [[True for _ in range(x_max)] for _ in range(y_max)]
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    (y, x) = (2 * randrange(y_max // 2) + 1, 2 * randrange(x_max // 2) + 1)
    grid[y][x] = False
    walls = {(y + dy, x + dx) for dy, dx in directions}
    while walls:
        y, x = sample(walls, 1)[0]
        walls.remove((y, x))
        if y == 0 or y == y_max - 1 or x == 0 or x == x_max - 1:
            continue
        if y % 2:
            y1 = y2 = y
            x1, x2 = x + 1, x - 1
        else:
            y1, y2 = y + 1, y - 1
            x1 = x2 = x
        if grid[y1][x1] != grid[y2][x2]:
            if grid[y1][x1]:
                grid[y1][x1] = grid[y][x] = False
                walls.update((y1 + dy, x1 + dx) for dy, dx in directions)
            else:
                grid[y2][x2] = grid[y][x] = False
                walls.update((y2 + dy, x2 + dx) for dy, dx in directions)
    return grid


def modified_prim(y_max: int, x_max: int) -> List[List[bool]]:
    """
    Modified Prim's 2D perfect maze generation algorithm
    :param y_max: height
    :param x_max: width
    :return: 2D perfect maze grid
    """
    assert y_max % 2 and x_max % 2 and y_max >= 3 and x_max >= 3
    grid = [[True for _ in range(x_max)] for _ in range(y_max)]
    directions = ((2, 0), (-2, 0), (0, 2), (0, -2))
    (y, x) = (2 * randrange(y_max // 2) + 1, 2 * randrange(x_max // 2) + 1)
    grid[y][x] = False
    cells = ((y + dy, x + dx) for dy, dx in directions)
    cells = {(y, x) for y, x in cells if 0 < y < y_max and 0 < x < x_max}
    while cells:
        y, x = sample(cells, 1)[0]
        cells.remove((y, x))
        neighbors = ((y + dy, x + dx) for dy, dx in directions)
        neighbors = [(y, x) for y, x in neighbors if 0 < y < y_max and 0 < x < x_max]
        ny, nx = choice([(y, x) for y, x in neighbors if not grid[y][x]])
        grid[y][x] = grid[(ny + y) // 2][(nx + x) // 2] = False
        cells.update(((y, x) for y, x in neighbors if grid[y][x]))
    return grid


def sidewinder(y_max: int, x_max: int, skew: float = 0.5) -> List[List[bool]]:
    """
    Sidewinder 2D perfect maze generation algorithm
    :param y_max: height
    :param x_max: width
    :param skew: if the skew is set less than 0.5 the maze will be skewed East-West, if it set greater than 0.5 it will
        be skewed North-South. (default 0.5)
    :return: 2D perfect maze grid
    """
    assert y_max % 2 and x_max % 2 and y_max >= 3 and x_max >= 3
    grid = [[True for _ in range(x_max)] for _ in range(y_max)]
    for x in range(1, x_max - 1):
        grid[1][x] = False
    for y in range(3, y_max, 2):
        run = []
        for x in range(1, x_max, 2):
            grid[y][x] = False
            run.append((y, x))
            carve_east = (random() >= skew)
            if carve_east and x < (x_max - 2):
                grid[y][x + 1] = False
            else:
                north = choice(run)
                grid[north[0] - 1][north[1]] = False
                run = []
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

    functions = [aldous_broder, wilson, binary_tree, backtracking, division, eller, growing_tree, kruskal,
                 prim, modified_prim, sidewinder]
    n_functions = ['Aldous-Broder algorithm', 'Wilson\'s algorithm', 'Binary tree algorithm',
                   'Backtracking algorithm', 'Division algorithm', 'Eller\'s algorithm', 'Growing tree algorithm',
                   'Kruskal\'s algorithm', 'Prim\'s algorithm', 'Prim\'s algorithm (modified)',
                   'Sidewinder algorithm']
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

