#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Implementation of algorithms for finding the shortest paths in 2D mazes.
    Algorithms:
    - A* algorithm
    - BFS (breadth-first search) (iterative version)
    - Dijkstra algorithm
"""

import heapq
from collections import deque
from math import inf
from typing import Callable, List, Tuple


class Heuristic:
    """
    A class with basic heuristics for the A * algorithm
    """

    @staticmethod
    def octile(y0, x0, y1, x1):
        (ty, tx) = (abs(y0 - y1), abs(x0 - x1))
        return max(ty, tx) + (2 ** 0.5 - 1) * min(ty, tx)

    @staticmethod
    def manhattan(y0, x0, y1, x1):
        return abs(y0 - y1) + abs(x0 - x1)

    @staticmethod
    def chebyshev(y0, x0, y1, x1):
        return max(abs(y0 - y1), abs(x0 - x1))

    @staticmethod
    def euclidean(y0, x0, y1, x1):
        return ((y0 - y1) ** 2 + (x0 - x1) ** 2) ** 0.5


def a_star(maze: List[List[bool]], beginNode: Tuple[int, int], endNode: Tuple[int, int],
           heuristic: Callable = Heuristic.manhattan) -> List[Tuple[int, int]]:
    """
    A* algorithm
    This implementation uses heapq - a priority queue.
    :param maze: 2D maze grid
    :param beginNode: initial position
    :param endNode: target position
    :param heuristic: heuristic function
    :return: path from initial to target position
    """
    current = (-1, -1)
    (y_max, x_max) = (len(maze), len(maze[0]))
    q = []
    cost = 0
    heapq.heappush(q, (cost, endNode))
    directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
    parentNode = {endNode: endNode}
    costMap = {endNode: cost}
    while q:
        current = heapq.heappop(q)[1]
        if current == beginNode:
            break
        cost = costMap[current] + 1
        for y_dir, x_dir in directions:
            (dy, dx) = (current[0] + y_dir, current[1] + x_dir)
            if dy >= y_max or dy < 0 or dx >= x_max or dx < 0 or maze[dy][dx]:
                continue
            neighbor = (dy, dx)
            if cost < costMap.get(neighbor, inf):
                costMap[neighbor] = cost
                parentNode[neighbor] = current
                heapq.heappush(q, (cost + heuristic(current[0], current[1], beginNode[0], beginNode[1]), neighbor))
    path = list()
    if current == beginNode:
        path.append(current)
        while current != endNode:
            current = parentNode[current]
            path.append(current)
    return path


def bfs(maze: List[List[bool]], beginNode: Tuple[int, int], endNode: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Breadth-first search algorithm (iterative version)
    (!) This implementation uses a deque instead of a queue. This choice is only related to the speed.
    :param maze: 2D maze grid
    :param beginNode: initial position
    :param endNode: target position
    :return: path from initial to target position
    """
    current = (-1, -1)
    (y_max, x_max) = (len(maze), len(maze[0]))
    q = deque()
    q.append(endNode)
    directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
    parentNode = {endNode: endNode}
    while q:
        current = q.popleft()
        if current == beginNode:
            break
        for y_dir, x_dir in directions:
            (dy, dx) = (current[0] + y_dir, current[1] + x_dir)
            if dy >= y_max or dy < 0 or dx >= x_max or dx < 0 or maze[dy][dx]:
                continue
            neighbor = (dy, dx)
            if neighbor not in parentNode:
                q.append(neighbor)
                parentNode[neighbor] = current
    path = list()
    if current == beginNode:
        path.append(current)
        while current != endNode:
            current = parentNode[current]
            path.append(current)
    return path


def dijkstra(maze: List[List[bool]], beginNode: Tuple[int, int], endNode: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Dijkstra algorithm
    This implementation uses heapq - a priority queue.
    :param maze: 2D maze grid
    :param beginNode: initial position
    :param endNode: target position
    :return: path from initial to target position
    """
    current = (-1, -1)
    (y_max, x_max) = (len(maze), len(maze[0]))
    q = []
    heapq.heappush(q, (0, endNode))
    directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
    parentNode = {endNode: endNode}
    costMap = {endNode: 0}
    while q:
        current = heapq.heappop(q)[1]
        if current == beginNode:
            break
        cost = costMap[current] + 1
        for y_dir, x_dir in directions:
            (dy, dx) = (current[0] + y_dir, current[1] + x_dir)
            if dy >= y_max or dy < 0 or dx >= x_max or dx < 0 or maze[dy][dx]:
                continue
            neighbor = (dy, dx)
            if cost < costMap.get(neighbor, inf):
                costMap[neighbor] = cost
                parentNode[neighbor] = current
                heapq.heappush(q, (cost, neighbor))
    path = list()
    if current == beginNode:
        path.append(current)
        while current != endNode:
            current = parentNode[current]
            path.append(current)
    return path

