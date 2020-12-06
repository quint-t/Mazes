#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Testing shortest path search algorithms in mazes
    2D perfect maze generation algorithms:
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
    2D imperfect maze generation algorithms:
    - Serpentine algorithm
    - Small rooms algorithm
    - Spiral algorithm
    Algorithms for finding the shortest paths in 2D mazes:
    - A* algorithm (4 heuristics)
    - BFS (breadth-first search) (iterative version)
    - Dijkstra algorithm
"""
from imperfect_maze import *
from perfect_maze import *
from solve_maze import *

import gc as garbage_collector
from random import randint, randrange
from time import process_time
from typing import Callable, List


def test_algorithms(n_tests: int, min_length: int, max_length: int, maze_functions: List[Callable],
                    maze_n_functions: List[str], solve_maze_functions: List[Callable],
                    solve_maze_n_functions: List[str], *, is_perfect_mazes: bool):
    maze_time_functions = [0 for _ in maze_functions]
    solve_maze_time_functions = [[0 for _ in maze_n_functions] for _ in solve_maze_n_functions]
    for i in range(n_tests):
        y_size, x_size = (randint(min_length, max_length) // 2) * 2 + 1, (
                randint(min_length, max_length) // 2) * 2 + 1
        for j, func in enumerate(maze_functions):
            garbage_collector.disable()
            maze_time_functions[j] -= process_time()
            maze = func(y_size, x_size)
            maze_time_functions[j] += process_time()
            garbage_collector.enable()
            (yFrom, xFrom, yTo, xTo) = 0, 0, 0, 0
            while maze[yFrom][xFrom] or maze[yTo][xTo] or (yFrom, xFrom) == (yTo, xTo):
                yFrom = randrange(y_size)
                xFrom = randrange(x_size)
                yTo = randrange(y_size)
                xTo = randrange(x_size)
            solve_results = []
            for k, solve_func in enumerate(solve_maze_functions):
                garbage_collector.disable()
                solve_maze_time_functions[k][j] -= process_time()
                result = solve_func(maze, (yFrom, xFrom), (yTo, xTo))
                solve_maze_time_functions[k][j] += process_time()
                garbage_collector.enable()
                solve_results.append(result)
                if is_perfect_mazes and not solve_results[k]:
                    print('Invalid answer or imperfect maze')
                    print(*[''.join('█' if col else ' ' for col in row) for row in maze], sep='\n')
                    print((yFrom, xFrom), (yTo, xTo))
                    print(solve_maze_n_functions[k], solve_results[k])
                    raise AttributeError
                if is_perfect_mazes and k and solve_results[k - 1] != solve_results[k] \
                        or not is_perfect_mazes and len(solve_results[k - 1]) != len(solve_results[k]):
                    print('Miscellaneous answers')
                    print(*[''.join('█' if col else ' ' for col in row) for row in maze], sep='\n')
                    print((yFrom, xFrom), (yTo, xTo))
                    print(solve_maze_n_functions[k - 1], solve_results[k - 1])
                    print(solve_maze_n_functions[k], solve_results[k])
                    raise AttributeError

    print('Time of execution of maze generation algorithms')
    for time, n in sorted(zip(maze_time_functions, maze_n_functions)):
        print(n + ': ' + str(time))
    print('\n' + 'Time of execution of algorithms to find the shortest paths in the mazes (briefly)')
    for time, sn in sorted(zip(solve_maze_time_functions, solve_maze_n_functions), key=lambda x: sum(x[0])):
        print(sn + ': ' + str(sum(time)))
    print('\n' + 'Time of execution of algorithms to find the shortest paths in the mazes (in detail)')
    for time, sn in sorted(zip(solve_maze_time_functions, solve_maze_n_functions), key=lambda x: sum(x[0])):
        print('#' * 30 + '\n' + 'Function:', sn)
        for n, t in sorted(zip(maze_n_functions, time), key=lambda x: x[1]):
            print(n + ': ' + str(t))


def main():
    def get_input(string, begin, end):
        string += f" ({begin}-{end}):"
        input_result = input(string)
        while not (input_result.isdecimal() and begin <= int(input_result) <= end):
            input_result = input(string)
        return int(input_result)

    print('=== Perfect algorithms ===')
    n_tests = get_input('Enter the number of tests', 1, 100000)
    min_length = get_input('Enter the minimum length of the maze (odd number)', 5, 100000)
    max_length = get_input('Enter the maximum length of the maze (odd number)', 5, 100000)
    maze_functions = [aldous_broder, wilson, backtracking, binary_tree, division, eller, growing_tree, kruskal,
                      prim, modified_prim, sidewinder]
    maze_n_functions = ['Aldous-Broder algorithm', 'Wilson\'s algorithm', 'Backtracking algorithm',
                        'Binary tree algorithm', 'Division algorithm', 'Eller\'s algorithm', 'Growing tree algorithm',
                        'Kruskal\'s algorithm', 'Prim\'s algorithm', 'Prim\'s algorithm (modified)',
                        'Sidewinder algorithm']
    solve_maze_functions = [bfs, dijkstra,
                            lambda mz, begin, end: a_star(mz, begin, end, Heuristic.octile),
                            lambda mz, begin, end: a_star(mz, begin, end, Heuristic.manhattan),
                            lambda mz, begin, end: a_star(mz, begin, end, Heuristic.chebyshev),
                            lambda mz, begin, end: a_star(mz, begin, end, Heuristic.euclidean)]
    solve_maze_n_functions = ['BFS algorithm', 'Dijkstra algorithm', 'A* algorithm (Octile heuristic)',
                              'A* algorithm (Manhattan heuristic)', 'A* algorithm (Chebyshev heuristic)',
                              'A* algorithm (Euclidean heuristic)']
    test_algorithms(n_tests, min_length, max_length, maze_functions, maze_n_functions, solve_maze_functions,
                    solve_maze_n_functions, is_perfect_mazes=True)

    print('\n', '=== Imperfect algorithms ===', sep='\n')
    n_tests = get_input('Enter the number of tests', 1, 100000)
    min_length = get_input('Enter the minimum length of the maze (odd number)', 5, 100000)
    max_length = get_input('Enter the maximum length of the maze (odd number)', 5, 100000)
    maze_functions = [serpentine, small_rooms, spiral]
    maze_n_functions = ['Serpentine algorithm', 'Small rooms algorithm', 'Spiral algorithm']
    test_algorithms(n_tests, min_length, max_length, maze_functions, maze_n_functions, solve_maze_functions,
                    solve_maze_n_functions, is_perfect_mazes=False)
    input()


if __name__ == '__main__':
    main()

